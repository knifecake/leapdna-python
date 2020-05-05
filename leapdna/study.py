from .utils import transpose, union, drop_nones

from .block import LeapdnaBlock
from .locus import Locus

class Study(LeapdnaBlock):
    __block_type__ = 'study'
    def __init__(self, loci = None, metadata = None, **rest):
        super().__init__(**rest)
        if loci is None: loci = []
        if metadata is None: metadata = {}

        for i, locus in enumerate(loci):
            if not isinstance(locus, Locus):
                loci[i] = Locus(**locus)

        self.loci = { locus.name: locus for locus in loci }
        self.metadata = metadata

    def get_freq(self, locus, allele):
        try:
            return self.loci[locus].alleles[allele].frequency
        except KeyError:
            return 0

    def all_locus_names(self):
        return set(self.loci.keys())

    def all_allele_names(self):
        return union(*[[allele.name for allele in locus.alleles.values()] for locus in self.loci.values()])

    def calculate_frequencies(self):
        for name in self.loci:
            self.loci[name].calculate_frequencies()

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
                    
            self.loci[locus['name']] = Locus(**locus)

    def to_leapdna(self, top_level = False):
        ret = super().to_leapdna(top_level)
        ret['loci'] = list(map(lambda l: l.to_leapdna(), self.loci.values()))
        return ret
    
    def __repr__(self):
        return '%s with %d loci' % (self.__class__, len(self.loci))

