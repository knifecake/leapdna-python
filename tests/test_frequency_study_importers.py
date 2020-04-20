import unittest
import json

from leapdna import FrequencyStudy

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

class TestFrequencyStudyImporters(unittest.TestCase):
    def test_table_import(self):
        fs = FrequencyStudy.from_file('examples/sample1.json')
        table = fs.to_table()

        self.assertEqual(FrequencyStudy.from_table(table).to_table(), table)

    def test_leapdna_import(self):
        with open('examples/sample1.json') as f:
            data = json.loads(f.read())
            fs = FrequencyStudy.from_leapdna(data)

            self.assertEqual(fs.to_table(), expected_loci)
            self.assertEqual(fs.metadata, expected_metadata)

    def test_tabular_file_import(self):
        fs = FrequencyStudy.from_tabular_file('examples/sample1.csv')
        self.assertEqual(fs.to_table(), expected_loci)

    def test_familias_file_import(self):
        fs = FrequencyStudy.from_familias_file('examples/sample1.txt')
        self.assertEqual(fs.to_table(), expected_loci)
