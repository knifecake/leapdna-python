import unittest

from leapdna import FrequencyStudy
from leapdna.importers import load_file 

class TestFrequencyStudy(unittest.TestCase):
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
        fs = FrequencyStudy()
        fs.from_table(expected)
        self.assertEqual(fs.to_table(), expected)

    def test_locus_tree(self):
        loci = [
            {'name': 'Locus 1', 'alleles': [
                { 'name': 'A1', 'frequency': 0.2 },
                { 'name': 'A2', 'frequency': 0.8 }
            ]},
            {'name': 'Locus 2', 'alleles': [
                { 'name': 'A2', 'frequency': 0.2 },
                { 'name': 'A3', 'frequency': 0.8 }
            ]}
        ]

        expected = {
            'Locus 1': {
                'name': 'Locus 1',
                'alleles': {
                    'A1': {
                        'name': 'A1',
                        'frequency': 0.2
                    },
                    'A2': {
                        'name': 'A2',
                        'frequency': 0.8
                    }
                }
            },
            'Locus 2': {
                'name': 'Locus 2',
                'alleles': {
                    'A2': {
                        'name': 'A2',
                        'frequency': 0.2
                    },
                    'A3': {
                        'name': 'A3',
                        'frequency': 0.8
                    }
                }
            }
        }

        self.assertEqual(FrequencyStudy._locus_tree(loci), expected)
