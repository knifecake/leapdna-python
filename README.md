# 👩‍🔬 leapdna python 🐍

An implementation of the leapdna toolkit in python.

## Installation

TODO

## Modules:

### Allele frequency datasets

Example usage:

```python
from leapdna import FrequencyStudy

# load a leapdna file
fs = FrequencyStudy.load_file('examples/sample1.json')

# load a tabular file in CSV format
fs = FrequencyStudy.load_tabular_file('examples/sample1.csv')

# load a Familias file
fs = FrequencyStudy.load_familias_file('examples/sample1.txt')

# convert to allelic ladder format
fs.to_table()

# convert to allelic ladder format but with loci in the rows
fs.to_table(rows = 'loci')

# get the frequency of a particular allele at a locus
fs.get_freq('Locus 1', 'Allele 1')
```

## Testing

You can run the tests from the project root by executing:

    python -m unittest discover -v

## License

&copy; 2020 Elias Hernandis

Leapdna is free and open-source sofware released under the [MIT
License](https://choosealicense.com/licenses/mit/). Everyone is free to copy,
modify and redistribute the sofware, even for commercial purposes. While no
attribution is required, it is very much appreciated. The full text of the
license is available
[here](https://github.com/knifecake/leapdna-python/blob/master/LICENSE).
