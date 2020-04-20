import unittest

from leapdna import FrequencyStudy

class TestFrequencyStudy(unittest.TestCase):
    def setUp(self):
        self.fs = FrequencyStudy.from_file('examples/sample1.json')

    def test_all_allele_names(self):
        expected = {'Allele 2', 'Allele B', 'Allele A', 'Allele 3', 'Allele 1', 'Allele 4'}
        self.assertEqual(self.fs.all_allele_names(), expected)

    def test_all_locus_names(self):
        expected = {'Locus 1', 'Locus 2', 'Locus 3'}
        self.assertEqual(self.fs.all_locus_names(), expected)

    def test_to_table(self):
        expected = [
            ['', 'Locus 1', 'Locus 2', 'Locus 3'],
            ['Allele 1', 0.8, 0, 0],
            ['Allele 2', 0.2, 0.5, 0],
            ['Allele 3', 0, 0.48, 0],
            ['Allele 4', 0, 0.02, 0],
            ['Allele A', 0, 0, 0.4],
            ['Allele B', 0, 0, 0.59]
        ]

        self.assertEqual(self.fs.to_table(), expected)
