import copy

from .block import LeapdnaBlock
from .allele import Allele
from .utils import drop_nones

class Locus(LeapdnaBlock):
    __block_type__ = 'locus'
    
    def __init__(self,
        name,
        alleles = None,
        sample_size = None,
        h_obs = None,
        h_exp = None,
        chrom = None,
        refseq_name = None,
        refseq_start = None,
        refseq_end = None,
        **rest):
        super().__init__(**rest)

        if alleles is None: alleles = []

        self.name = name
        for i, allele in enumerate(alleles):
            if not isinstance(allele, Allele):
                alleles[i] = Allele(**allele)

        self.alleles = { allele.name: allele for allele in alleles }
        self.sample_size = sample_size
        self.h_obs = h_obs
        self.h_exp = h_exp
        self.chrom = chrom
        self.refseq_name = refseq_name
        self.refseq_start = refseq_start
        self.refseq_end = refseq_end    

    @property
    def h_obs(self):
        return self.dprops['h_obs']

    @h_obs.setter
    def h_obs(self, value):
        assert value is None or 0 <= value and value <= 1, "h_obs is not between 0 and 1"
        self.dprops['h_obs'] = value
    
    @property
    def h_exp(self):
        if self.dprops['h_exp'] is None:
            self.dprops['h_exp'] = 1 - sum(map(lambda a: a.frequency**2, self.alleles.values()))

        return self.dprops['h_exp']

    @h_exp.setter
    def h_exp(self, value):
        assert value is None or 0 <= value and value <= 1, "h_exp is not between 0 and 1"
        self.dprops['h_exp'] = value

    def to_leapdna(self, top_level = False):
        ret = super().to_leapdna(top_level)
        ret['alleles'] = list(map(lambda a: a.to_leapdna(), self.alleles.values()))
        return ret

    @property
    def sample_size(self):
        if self.dprops['sample_size'] is None:
            try:
                self.dprops['sample_size'] = self._sample_size_sum()
            except TypeError:
                raise ValueError(f'some alleles have missing sample counts for locus {self.name}')

        return self.dprops['sample_size']
    
    @sample_size.setter
    def sample_size(self, value):
        assert value is None or isinstance(value, int) and value >= 0, "sample size is not a non-negative integer"
        self.dprops['sample_size'] = value
    
    def calculate_frequencies(self):
        for name in self.alleles:
            self.alleles[name].frequency = self.alleles[name].count / self.sample_size

    def _allele_frequency_sum(self):
        return sum(map(lambda a: a.frequency, self.alleles.values()))

    def _sample_size_sum(self):
        return sum(map(lambda a: a.count, self.alleles.values()))
