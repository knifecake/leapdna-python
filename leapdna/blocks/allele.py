from typing import Union

from leapdna.blocks.base import Base
from leapdna.blocks.locus import Locus


class Allele(Base):
    block_type: str = 'allele'
    name: str
    locus: Locus

    def __init__(self, name: str, locus: Union[Locus, str], *args, **kwargs):
        super().__init__(block_type=self.block_type, *args,
                         **kwargs)  # type: ignore

        self.name = name
        if isinstance(locus, Locus):
            self.locus = locus
        else:
            self.locus_id = locus

    def resolve_deps_from_blob(self, blob):
        if self.locus_id and self.locus_id in blob:
            self.locus = blob[self.locus_id]

    def __str__(self):
        return f'<{self.block_type.capitalize()}: {self.name}@{self.locus}>'
