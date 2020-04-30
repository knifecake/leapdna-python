import unittest

from leapdna.allele import Allele
from leapdna.sequence import Sequence

class TestAllele(unittest.TestCase):
    def test_allele_supports_ce(self):
        cea = Allele(ce_name = '13.2', frequency = 0.2, locus_name = 'vWA')
        self.assertEqual(cea.name, '13.2')
        self.assertEqual(cea.frequency, 0.2)
        self.assertEqual(cea.locus_name, 'vWA')

    def test_allele_setting_name_takes_precedence(self):
        a = Allele(ce_name = 'wrong')
        self.assertEqual(a.name, 'wrong')

        a.name = 'right'
        self.assertEqual(a.name, 'right')

    def test_sequence_name_bubbles_up(self):
        sq = Sequence(name = 'seqname')
        a = Allele(sequence = sq)
        self.assertEqual(a.name, sq.name)

    def test_leapdna_supports_ce(self):
        cea = Allele(ce_name = '13.2', frequency = 0.2, locus_name = 'vWA')
        res = cea.to_leapdna()

        expected = {
            'ce_name': '13.2',
            'frequency': 0.2,
            'locus_name': 'vWA',
            'type': 'allele'
        }

        self.assertEqual(cea.to_leapdna(), expected)

        force_name_calc = cea.name

        self.assertEqual(cea.to_leapdna()['name'], '13.2')



