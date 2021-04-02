# 👩‍🔬 leapdna.py

An implementation of the leapdna toolkit in Python.

## Installation

leapdna is compatible with Python 3.9 and greater. Install it from PyPI with

    pip install leapdna


## Usage

### Working with data

leapdna aims to provide a way to represent a lot of the data that is normally dealt with in genetics, with a focus on forensic applications. The usual suspects here are loci, alleles, profiles, allele frequency studies... All of these are represented in leapdna by a block. A block is a Python class which can be stored as a JSON file with the leapdna format. All blocks inherit from the `Base` block class and define some attributes and functionality of their own. For instance, a `Locus` block has a `name` attribute, in addition to a `band` attribute, which specifies the [chromosome band](https://www.ncbi.nlm.nih.gov/Class/MLACourse/Original8Hour/Genetics/chrombanding.html "NCBI article on chromosome banding and nomenclature") where the locus is. Other `Locus` blocks will have different values for these attributes while other types of blocks, such as `Allele`, will have a different set of attributes altogether. The documentation details which attributes are supported (and sometimes required) for a particular block type.

```python
from leapdna.blocks import Allele, Locus


l1 = Locus('L1')
a1 = Allele(name='a1', locus=l1)
```

leapdna aims to be extensible, so it allows you to specify your own attributes in any kind of block. If you wanted to mark a locus as a potential carrier of a diseas you could do

```python
l1.user['carrier'] = True
```

## Testing

To run the leapdna test suite execute

```bash
python3 -m unittest
```

from the root of the leapdna repository.

In addition, leapdna comes with type annotations which allows for running it through a type checker such as `mypy`. This can be done by executing `mypy leapdna` from the root of the repository. If you do not have `mypy` installed you may do so with `python3 -m pip install mypy`.

## License

Copyright 2021 Elias Hernandis

Leapdna is free and open-source sofware released under the [MIT License](https://choosealicense.com/licenses/mit/ "A human-friendly overview of the MIT license"). Everyone is free to copy, modify and redistribute the sofware, even for commercial purposes. While no attribution is required, it is very much appreciated. The full text of the license is available [here](https://github.com/knifecake/leapdna-python/blob/master/LICENSE "Full text of the leapdna license (MIT License)").
