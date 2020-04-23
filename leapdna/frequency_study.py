import json
import csv

from .utils import transpose, union

class FrequencyStudy():
    def __init__(self, loci = [], metadata = {}): 
        self.loci = FrequencyStudy._locus_tree(loci)
        self.metadata = metadata

    def get_freq(self, locus, allele):
        try:
            return self.loci[locus]['alleles'][allele]['frequency']
        except KeyError:
            return 0

    def all_locus_names(self):
        return set(self.loci.keys())

    def all_allele_names(self):
        return union(*(list(locus['alleles'].keys()) for locus in self.loci.values()))

    def to_table(self):
        table = []
        row_headers = sorted(self.all_allele_names())
        column_headers = sorted(self.all_locus_names())

        # first row is a header with the locus names
        table.append([''] + column_headers)

        # build the table
        for allele in row_headers:
            # first column is a header with the allele names
            row = [allele]
            for locus in column_headers:
                row.append(self.get_freq(locus, allele))
            table.append(row)

        return table

    def from_table(self, table):
        # it's just easier to work with wide tables
        table = transpose(table)
        
        allele_index = table[0]
        loci = []
        for row in table[1:]:
            locus = { 'name' : row[0], 'alleles': [] }
            for (i, frequency) in enumerate(row[1:]):
                if frequency:
                    locus['alleles'].append({
                        'name': allele_index[i + 1],
                        'frequency': float(frequency)
                    })
            loci.append(locus)

        self.loci = self._locus_tree(loci)

    @classmethod
    def from_leapdna(cls, json):
        return FrequencyStudy(json.get('loci', []), json.get('metadata', {}))

    @staticmethod
    def _locus_tree(loci):
        for locus in loci:
            named_alleles = { 'alleles': { allele['name']: allele
                for allele in locus['alleles'] }}
            locus.update(named_alleles)

        return { locus['name']: locus for locus in loci }

    def __repr__(self):
        return '%s with %d loci' % (self.__class__, len(self.loci))

