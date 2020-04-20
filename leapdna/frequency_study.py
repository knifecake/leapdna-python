import json
import operator
from functools import reduce

transpose = lambda matrix: list(map(list, zip(*matrix)))
union = lambda lists: set(reduce(operator.add, lists))

class FrequencyStudy():
    def __init__(self, metadata = {}, loci = []):
        self.metadata = metadata
        self.loci = FrequencyStudy._name_loci(loci)

    def to_table(self, na_value = 0, rows = 'alleles' ):
        table = []
        row_headers = sorted(self.all_allele_names())
        column_headers = sorted(self.all_locus_names())
        table.append([''] + column_headers)

        # build the table
        for allele in row_headers:
            row = [allele]
            for locus in column_headers:
                row.append(self.get_freq(locus, allele, default = na_value))
            table.append(row)

        if rows == 'alleles':
            pass
        elif rows == 'loci':
            table = transpose(table)
        else:
            raise ValueError('The value for the \'rows\' option was not understood')

        return table

    def get_freq(self, locus, allele, default = 0):
        try:
            return self.loci[locus]['alleles'][allele]['frequency']
        except KeyError:
            return default

    def all_locus_names(self):
        return set(self.loci.keys())

    def all_allele_names(self):
        return union([list(locus['alleles'].keys()) for locus in self.loci.values()])

    @classmethod
    def from_leapdna(cls, json):
        return FrequencyStudy(json['metadata'], json['loci'])

    @classmethod
    def from_file(cls, path, mode = 'auto', options = {}):
        with open(path) as f:
            contents = f.read()
            if mode == 'auto':
                mode = cls.guess_filetype(path, contents)

            if mode == 'json':
                obj = json.loads(contents)
                return cls.from_leapdna(obj)
            else:
                print('File type not recognised')

    @staticmethod
    def guess_filetype(path, contents):
        if '.json' in path:
            guess = 'json'
        else:
            guess = 'unknown'

        return guess

    @staticmethod
    def _name_loci(loci):
        for old_locus in loci:
            named_alleles = { 'alleles': { al['name']: al for al in old_locus['alleles'] }}
            old_locus.update(named_alleles)

        return { locus['name']: locus for locus in loci }

    def __repr__(self):
        return '%s with %d loci' % (self.__class__, len(self.loci))

