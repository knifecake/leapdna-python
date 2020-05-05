import csv
import json
import copy
from io import StringIO

from .utils import replace
from .allele import Allele
from .locus import Locus
from .study import Study

__all__ = [
    'import_leapdna',
    'import_familias',
    'import_tabular',
    'load_leapdna_file',
    'load_familias_file',
    'load_tabular_file',
    'load_file',
    'guess_filetype'
]

def import_leapdna(contents):
    if isinstance(contents, str):
        contents = json.loads(contents)
    else:
        contents = copy.deepcopy(contents)

    if contents['type'] == 'study':
        contents.update({
            'loci': list(map(import_leapdna, contents['loci']))
        })
        return Study(**contents)
    elif contents['type'] == 'locus':
        contents.update({
            'alleles': list(map(import_leapdna, contents['alleles']))
        })
        return Locus(**contents)
    elif contents['type'] == 'allele':
        return Allele(**contents)
    elif contents['type'] == 'block':
        return LeapdnaBlock(**contents)
    else:
        raise ValueError('Leapdna block type not recognized')

    

def import_familias(contents):
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
        
    return Study(loci)

def import_tabular(contents, dialect = 'guess', row_indexing = 'guess', na_string = ''):
    if row_indexing not in ('alleles', 'loci', 'guess'):
        raise ValueError('Invalid \'rows\' parameter. Must be one of "alleles", "loci" or "guess".')

    if dialect == 'guess':
        dialect = csv.Sniffer().sniff(contents)

    reader = csv.reader(StringIO(contents), dialect)
    table = list(reader)

    if na_string != '':
        table = replace(table, na_string, 0)

    if row_indexing == 'loci':
        table = transpose(table)
    elif row_indexing == 'guess':
        # tables with alleles in rows are longer than wider
        # use this to guess if we should transpose the table
        if len(table) < len(table[0]):
            table = transpose(table)

    fs = Study()
    fs.from_table(table)
    return fs

def load_leapdna_file(path):
    with open(path) as f:
        fs = import_leapdna(f.read())
        return fs

def load_familias_file(path, metadata = {}):
    with open(path) as f:
        fs = import_familias(f.read())
        fs.metadata = metadata
        return fs

def load_tabular_file(path, metadata = {}, **kwargs):
    with open(path) as f:
        fs = import_tabular(f.read(), **kwargs)
        fs.metadata = metadata
        return fs

def load_file(path, mode = 'auto', metadata = {}, **kwargs):
    with open(path) as f:
        contents = f.read()
        
        # guess file type if asked
        if mode == 'auto':
            mode = guess_filetype(path, contents)

        # invoke the appripriate loader
        if mode == 'leapdna':
            return import_leapdna(contents)
        elif mode == 'familias':
            return import_familias(contents)
        elif mode == 'tabular':
            return import_tabular(contents, **kwargs)
        else:
            raise AssertionError('File type not recognised')

def guess_filetype(path, contents):
    if '.json' in path or 'leapdna' in path:
        guess = 'leapdna'
    elif '.csv' in path or '.tsv' in path:
        guess = 'tabular'
    elif '.txt' in path:
        # TODO: be more sophisticated
        guess = 'familias'

    return guess

