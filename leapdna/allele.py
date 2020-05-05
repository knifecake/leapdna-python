from .block import LeapdnaBlock

class Allele(LeapdnaBlock):
    __block_type__ = 'allele'

    def __init__(self,
        name = None,
        locus_name = None,
        frequency = None,
        count = None,
        **rest):

        super().__init__(**rest)

        self._name = name
        self.locus_name = locus_name
        self.frequency = frequency
        self.count = count

    @property
    def name(self):
        if self._name is not None:
            return self._name

        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def to_leapdna(self, top_level = False):
        ret = super().to_leapdna(top_level)
        if self._name is not None:
            ret['name'] = self._name

        return ret

class SequenceAllele(Allele):
    __block_type__ = 'seq_allele'

    def __init__(self, sequence, **rest):
        rest['name'] = rest.get('name', sequence.name)
        super().__init__(**rest)
        self.sequence = sequence

    def to_leapdna(self, top_level = False):
        ret = super().to_leapdna(top_level)
        ret['sequence'] = self.sequence.to_leapdna(False)
        return ret
