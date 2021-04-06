from typing import Optional
from leapdna.blocks.base import Base

from leapdna.map import Coords, band2coords


class Locus(Base):
    block_type = 'locus'
    name: str
    coords: Optional[Coords]
    band: Optional[str]

    def __init__(self,
                 name: str,
                 coords: Optional[Coords] = None,
                 band: Optional[str] = None,
                 id: Optional[str] = None,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore
        self.coords = coords
        self.band = band
        self.name = name
        self.id = id or self.name

    def get_coords(self, guess=True):
        """Returns a triple (chr, start, stop) with the coordinates of the locus
        as given by coords. If coords is not set but band is, and guess is not False,
        then an attempt is made to convert the known band into such a triple using GRCh38."""

        if self.coords:
            return self.coords
        if guess and self.band:
            return band2coords(self.band)
        return None

    def asdict(self, without_deps=False):
        ret = super().asdict(without_deps=without_deps)
        ret.update({
            'name': self.name,
            'band': self.band,
            'coords': self.coords
        })
        return ret
