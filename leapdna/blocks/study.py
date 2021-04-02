from leapdna.blocks import locus
from leapdna.blocks.allele import Allele
from leapdna.blocks.locus import Locus
from typing import Dict, Optional, Sequence, Union

from leapdna.blocks.base import Base
from leapdna.blocks.observation import Observation


class Study(Base):
    block_type: str = 'study'
    observation_list: Sequence[Observation]
    observation_ids: Sequence[str]
    allele_index: Dict[Allele, Observation]

    def __init__(self, observations: Sequence[Union[Observation, str]], *args,
                 **kwargs):
        super().__init__(block_type=self.block_type, *args,
                         **kwargs)  # type: ignore

        if all(isinstance(obs, Observation) for obs in observations):
            self.observation_ids = []
            self.observation_list = observations  # type: ignore
            self.calculate_frequencies()
            self.rebuild_indices()
        else:
            self.observation_ids = observations  # type: ignore
            self.observation_list = []

    def resolve_deps_from_blob(self, blob):
        def _resolve_observation(obs):
            if isinstance(obs, str) and obs in blob:
                return blob[obs]

            return obs

        self.observation_list = [
            _resolve_observation(item) for item in self.observation_ids
        ]
        self.rebuild_indices()

    def rebuild_indices(self):
        self.allele_index = {obs.allele: obs for obs in self.observation_list}

    def calculate_frequencies(self):
        assert all(obs.count is not None for obs in self.observation_list),\
            'All observations must have a count'

        loci = set([obs.allele.locus for obs in self.observation_list])
        total_count_per_locus = {
            locus: sum(obs.count for obs in self.observation_list
                       if obs.allele.locus == locus)
            for locus in loci
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