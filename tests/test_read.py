import unittest
import json

from leapdna import Study
from leapdna.read import *

expected_loci = [
    ['', 'Locus 1', 'Locus 2', 'Locus 3'],
    ['Allele 1', 0.8, 0, 0],
    ['Allele 2', 0.2, 0.5, 0],
    ['Allele 3', 0, 0.48, 0],
    ['Allele 4', 0, 0.02, 0],
    ['Allele A', 0, 0, 0.4],
    ['Allele B', 0, 0, 0.59]
]

expected_metadata = {
    "name": "A sample study",
    "population": "Alderaan",
    "publication": {
      "authors": "Hernandis, E. et al.",
      "doi": "10.1109/5.771073",
      "date": "2020-04-20",
      "url": "https://doi.org/10.1109/5.771073"
    }
}

class TestStudyImporters(unittest.TestCase):
    def test_load_tabular_file(self):
        fs = load_tabular_file('tests/stubs/sample1.csv',)
        self.assertEqual(fs.to_table(), expected_loci)

    def test_load_tabular_file_with_custom_na_value(self):
        fs = load_tabular_file('tests/stubs/sample1-na.csv', na_string = 'NA')
        self.assertEqual(fs.to_table(), expected_loci)

    def test_leapdna_import_study(self):
        with open('tests/stubs/sample1.json') as f:
            data = json.loads(f.read())
            fs = import_leapdna(data)

            self.assertEqual(fs.to_table(), expected_loci)
            self.assertEqual(fs.metadata, expected_metadata)

    def test_leapdna_import_study2(self):
        with open('tests/stubs/study.leapdna.json') as f:
            data = json.loads(f.read())
            fs = import_leapdna(data)

            self.maxDiff = None
            self.assertEqual(fs.to_leapdna(), data)

    def test_load_familias_file(self):
        fs = load_familias_file('tests/stubs/sample1.txt')
        self.assertEqual(fs.to_table(), expected_loci)

    def test_filetype_guess(self):
        csv_path = 'tests/stubs/sample1.csv'
        with open(csv_path) as csv_file:
            self.assertEqual(guess_filetype(csv_path, csv_file), 'tabular')

        familias_path = 'tests/stubs/sample1.txt'
        with open(familias_path) as familias_file:
            self.assertEqual(guess_filetype(familias_path, familias_file), 'familias')
