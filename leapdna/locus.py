import copy

from .allele import Allele
from .utils import drop_nones

class Locus():
    def __init__(self, name, alleles = None, **user):
        if alleles is None: alleles = []

        self.name = name
        for i, allele in enumerate(alleles):
            if not isinstance(allele, Allele):
                alleles[i] = Allele(**allele)

        self.alleles = { allele.name: allele for allele in alleles }

    def to_leapdna(self):
        ret = drop_nones(self.__dict__)
        ret['alleles'] = list(map(lambda a: a.to_leapdna(), self.alleles.values()))
        return ret

    # pretend to be a dictionary
    def __getitem__(self, index):
        return self.__dict__[index]

    def __setitem__(self, index, value):
        self.__dict__[index] = value