import copy

from .allele import Allele
from .utils import drop_nones

class Locus():
    def __init__(self,
        name,
        alleles = None,
        sample_size = None,
        h_obs = None,
        h_exp = None,
        chrom = None,
        refseq_start = None,
        refseq_end = None,
        refseq_name = None,
        **user):
        if alleles is None: alleles = []

        self.name = name
        self.chrom = chrom
        self.refseq_name = refseq_name
        self.refseq_start = refseq_start
        self.refseq_end = refseq_end
        self.dprops = {
            'h_obs': h_obs,
            'h_exp': h_exp,
            'sample_size': sample_size
        }

        for i, allele in enumerate(alleles):
            if not isinstance(allele, Allele):
                alleles[i] = Allele(**allele)

        self.alleles = { allele.name: allele for allele in alleles }

    @property
    def h_obs(self):
        return self.dprops['h_obs']

    @h_obs.setter
    def h_obs(self, value):
        assert 0 <= value and value <= 1
        self.dprops['h_obs'] = value
    
    @property
    def h_exp(self):
        if self.dprops['h_exp'] is None:
            self.dprops['h_exp'] = 1 - sum(map(lambda a: a.frequency**2, self.alleles.values()))

        return self.dprops['h_exp']

    @h_exp.setter
    def h_exp(self, value):
        assert 0 <= value and value <= 1
        self.dprops['h_exp'] = value

    def to_leapdna(self):
        ret = drop_nones(self.__dict__)
        ret['alleles'] = list(map(lambda a: a.to_leapdna(), self.alleles.values()))
        del ret['dprops']
        ret.update(drop_nones(self.dprops))
        return ret

    @property
    def sample_size(self):
        if self.dprops['sample_size'] is None:
            try:
                self.dprops['sample_size'] = sum(map(lambda a: a.count, self.alleles.values()))
            except TypeError:
                raise ValueError(f'some alleles have missing sample counts for locus {self.name}')

        return self.dprops['sample_size']
    
    @sample_size.setter
    def sample_size(self, value):
        assert isinstance(value, int) and value >= 0
        self.dprops['sample_size'] = value
    
    def calculate_frequencies(self):
        for name in self.alleles:
            self.alleles[name].frequency = self.alleles[name].count / self.sample_size

    # pretend to be a dictionary
    def __getitem__(self, index):
        return self.__dict__[index]

    def __setitem__(self, index, value):
        self.__dict__[index] = value