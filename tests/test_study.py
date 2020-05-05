import unittest

from leapdna import Study
from leapdna.read import load_file 

class TestStudy(unittest.TestCase):
    def setUp(self):
        self.fs = load_file('tests/stubs/sample1.json')

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

    def test_from_table(self):
        expected = [
            ['', 'Locus 1', 'Locus 2', 'Locus 3'],
            ['Allele 1', 0.8, 0, 0],
            ['Allele 2', 0.2, 0.5, 0],
            ['Allele 3', 0, 0.48, 0],
            ['Allele 4', 0, 0.02, 0],
            ['Allele A', 0, 0, 0.4],
            ['Allele B', 0, 0, 0.59]
        ]
        fs = Study()
        fs.from_table(expected)
        self.assertEqual(fs.to_table(), expected)

    def test_calculate_frequencies(self):
        fs = Study([{'name': 'L1', 'alleles': [{'name': 'A', 'count': 5}, {'name': 'B', 'count': 5}]}])
        fs.calculate_frequencies()

        self.assertEqual(fs.loci['L1'].alleles['A'].frequency, 0.5)
        self.assertEqual(fs.loci['L1'].alleles['B'].frequency, 0.5)

    def test_leapdna(self):
        fs = Study([{'name': 'L1', 'alleles': [{'name': 'A', 'count': 5}]}])
        expected = {
            'type': 'study',
            'metadata': {},
            'loci': [
                {
                    'type': 'locus', 
                    'name': 'L1',
                    'alleles': [
                        { 'type': 'allele', 'name': 'A', 'count': 5 }
                    ]
                }
            ]
        }

        self.assertEqual(fs.to_leapdna(), expected)
