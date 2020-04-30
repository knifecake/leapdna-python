from .block import LeapdnaBlock

class Allele(LeapdnaBlock):
    __block_type__ = 'allele'

    def __init__(self,
        name = None,
        ce_name = None,
        locus_name = None,
        sequence = None,
        frequency = None,
        count = None,
        **rest):

        super().__init__(**rest)

        self._name = name
        self.ce_name = ce_name
        self.locus_name = locus_name
        self.sequence = sequence
        self.frequency = frequency
        self.count = count

    @property
    def name(self):
        if self._name is not None:
            return self._name

        if self.sequence is not None:
            self._name = self.sequence.name
        elif self.ce_name is not None:
            self._name = self.ce_name
        
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def to_leapdna(self, top_level = False):
        ret = super().to_leapdna(top_level)
        if self._name is not None:
            ret['name'] = self._name

        return ret

