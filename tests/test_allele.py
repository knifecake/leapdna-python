import unittest

from leapdna.allele import Allele

class TestAllele(unittest.TestCase):
    def test_allele_to_leapdna(self):
        self.assertEqual(Allele('name').to_leapdna(), {'name': 'name'})
        self.assertEqual(Allele('name', frequency = 0.3).to_leapdna(),
            {'name': 'name', 'frequency': 0.3})
        self.assertEqual(Allele('name', **{'my_param': 34}).to_leapdna(),
            {'name': 'name', 'user': {'my_param': 34}})