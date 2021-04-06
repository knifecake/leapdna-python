from leapdna.blocks.locus import Locus
from typing import Optional, Union
from .base import Base
from .allele import Allele


class Observation(Base):
    block_type = 'observation'
    allele: Allele
    count: Optional[int]
    frequency: Optional[float]

    def __init__(self,
                 allele: Union[Allele, str],
                 count: Optional[int] = None,
                 frequency: Optional[float] = None,
                 id: Optional[str] = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore
        if isinstance(allele, Allele):
            self.allele = allele
        else:
            self.allele_id = allele

        self.count = count
        self.frequency = frequency
        self.id = id or f'obs_{self.allele.id}'

    @property
    def locus(self) -> Locus:
        return self.allele.locus

    def resolve_deps_from_blob(self, blob):
        if self.allele_id and self.allele_id in blob:
            self.allele = blob[self.allele_id]

    def asdict(self, without_deps=False):
        ret = super().asdict(without_deps=without_deps)
        ret.update({
            'allele': self.allele.id,
            'count': self.count,
            'frequency': self.frequency
        })

        if without_deps:
            ret['allele'] = self.allele.asdict(without_deps=True)

        return ret

    def block_deps(self):
        ret = {self.allele.id: self.allele}
        ret.update(self.allele.block_deps())
        return ret