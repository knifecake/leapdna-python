from typing import Any, Dict, Optional, Sequence, Union

from leapdna.blocks.allele import Allele
from leapdna.blocks.base import Base
from leapdna.blocks.observation import Observation
from leapdna.blocks.locus import Locus
from leapdna.errors import LeapdnaError


class Study(Base):
    block_type: str = 'study'
    observation_list: Sequence[Observation]
    observation_ids: Sequence[str]
    loci_metadata: Dict[str, Dict]
    allele_index: Dict[Allele, Observation]
    name: Optional[str]
    sample_size: Optional[int]
    metadata: Dict[str, Any]

    def __init__(self,
                 observations: Sequence[Union[Observation, str]],
                 name: Optional[str] = None,
                 id: Optional[str] = None,
                 sample_size: Optional[int] = None,
                 loci_metadata: Optional[Dict[str, Dict]] = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore

        if all(isinstance(obs, Observation) for obs in observations):
            self.observation_ids = \
                [obs.id for obs in observations]  # type: ignore
            self.observation_list = observations  # type: ignore
            self.rebuild_indices()
        else:
            self.observation_ids = observations  # type: ignore
            self.observation_list = []

        self.id = id or name or 'study_default_id'
        self.name = name
        self.sample_size = sample_size
        self.loci_metadata = loci_metadata or {}

    def resolve_deps_from_blob(self, blob):
        def _resolve_observation(obs):
            if isinstance(obs, str) and obs in blob:
                return blob[obs]

            raise LeapdnaError(f'Could not resolve observation "{obs}".')

        self.observation_list = [
            _resolve_observation(item) for item in self.observation_ids
        ]
        self.rebuild_indices()

    def rebuild_indices(self):
        self.allele_index = {obs.allele: obs for obs in self.observation_list}

    def calculate_frequencies(self):
        assert all(obs.count is not None for obs in self.observation_list),\
            'All observations must have a count'

        _loci = set([obs.allele.locus for obs in self.observation_list])
        total_count_per_locus = {
            locus: sum(obs.count for obs in self.observation_list
                       if obs.allele.locus == locus)
            for locus in _loci
        }

        for i, obs in enumerate(self.observation_list):
            self.observation_list[i].frequency = \
                obs.count / total_count_per_locus[obs.allele.locus]

    def get_freq(self, allele: Allele) -> float:
        if not self.allele_index:
            self.rebuild_indices()

        try:
            return self.allele_index[allele].frequency or 0
        except KeyError:
            return 0

    def get_freq_by_names(self, locus_name: str, allele_name: str) -> float:
        obs = [
            obs for obs in self.observation_list
            if obs.allele.name == allele_name
            and obs.allele.locus.name == locus_name
        ]

        try:
            return obs[0].frequency or 0
        except IndexError:
            return 0

    def prefix_observation_ids(self, id=None):
        if id is None:
            id = self.id
        for obs in self.observation_list:
            obs.id = id + '_' + obs.id
        self.observation_ids = [obs.id for obs in self.observation_list]

    @property
    def loci(self):
        return set(obs.locus for obs in self.observation_list)

    def asdict(self, without_deps=False):
        ret = super().asdict(without_deps=without_deps)
        ret.update({
            'observations': self.observation_ids,
            'name': self.name,
            'loci_metadata': self.loci_metadata
        })
        if without_deps:
            ret['observations'] = [
                obs.asdict(without_deps=True) for obs in self.observation_list
            ]
        return ret

    def block_deps(self):
        if not self.observation_list: return {}

        ret = {}
        for obs in self.observation_list:
            ret.update(obs.block_deps())
            ret[obs.id] = obs

        return ret
