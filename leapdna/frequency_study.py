import json
import csv
import operator
from functools import reduce

transpose = lambda matrix: list(map(list, zip(*matrix)))
union = lambda lists: set(reduce(operator.add, lists))

class FrequencyStudy():
    def __init__(self, loci = [], metadata = {}): 
        self.loci = FrequencyStudy._name_loci(loci)
        self.metadata = metadata

    def get_freq(self, locus, allele, default = 0):
        try:
            return self.loci[locus]['alleles'][allele]['frequency']
        except KeyError:
            return default

    def all_locus_names(self):
        return set(self.loci.keys())

    def all_allele_names(self):
        return union([list(locus['alleles'].keys()) for locus in self.loci.values()])

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
            raise ValueError('Invalid \'rows\' parameter. Must be one of "alleles" or "loci".')

        return table

    @classmethod
    def from_table(cls, table, metadata = {}, rows = 'alleles', na_value = ''):
        if rows == 'alleles':
            table = transpose(table)
        elif rows == 'loci':
            pass
        else:
            raise ValueError('Invalid \'rows\' parameter. Must be one of "alleles" or "loci".')

        allele_index = table[0]
        loci = []
        for row in table[1:]:
            locus = { 'name' : row[0], 'alleles': [] }
            for (i, frequency) in enumerate(row[1:]):
                if frequency != na_value and frequency != 0:
                    locus['alleles'].append({
                        'name': allele_index[i + 1],
                        'frequency': float(frequency)
                    })
            loci.append(locus)

        return cls(loci, metadata)

    @classmethod
    def from_leapdna(cls, json):
        return FrequencyStudy(json['loci'], json['metadata'])

    @classmethod
    def from_familias(cls, contents, metadata = {}, newline = '\n'):
        loci = []
        current_locus = None
        for line in contents.split('\n'):
            if current_locus is None:
                current_locus = { 'name': line, 'alleles': [] }
            else:
                if line == '':
                    loci.append(current_locus)
                    current_locus = None
                else:
                    name, frequency = line.split('\t')
                    current_locus['alleles'].append({
                        'name': name,
                        'frequency': float(frequency)
                    })

        return cls(loci, metadata)

    @classmethod
    def from_tabular_file(cls, path, metadata = {}, dialect = 'guess', rows = 'alleles', na_value = ''):
        with open(path) as f:
            if dialect == 'guess':
                dialect = csv.Sniffer().sniff(f.read())
                f.seek(0)

            reader = csv.reader(f, dialect)
            return cls.from_table(list(reader), metadata, rows, na_value)


    @classmethod
    def from_familias_file(cls, path, metadata = {}):
        with open(path) as f:
            return cls.from_familias(f.read(), metadata)

    @classmethod
    def from_file(cls, path, mode = 'auto', metadata = {}):
        with open(path) as f:
            contents = f.read()
            if mode == 'auto':
                mode = cls.guess_filetype(path, contents)

            if mode == 'json':
                obj = json.loads(contents)
                return cls.from_leapdna(obj)
            else:
                raise AssertionError('File type not recognised')

    @staticmethod
    def guess_filetype(path, contents):
        if '.json' in path:
            guess = 'json'
        elif 'csv' in path or 'tsv' in path:
            guess = 'tabular'

        return guess

    @staticmethod
    def _name_loci(loci):
        for old_locus in loci:
            named_alleles = { 'alleles': { al['name']: al for al in old_locus['alleles'] }}
            old_locus.update(named_alleles)

        return { locus['name']: locus for locus in loci }

    def __repr__(self):
        return '%s with %d loci' % (self.__class__, len(self.loci))

