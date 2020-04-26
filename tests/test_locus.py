import unittest

from leapdna.locus import Locus
from leapdna.allele import Allele

class TestLocus(unittest.TestCase):
    def test_to_leapdna(self):
        self.assertEqual(Locus('name').to_leapdna(), {'name': 'name', 'alleles': []})
        self.assertEqual(Locus('name', [{'name':'a'}, {'name':'b'}]).to_leapdna(),
            {'name': 'name', 'alleles': [{'name':'a'}, {'name':'b'}]})

    def test_to_leapdna_moves_dprops_to_top_level(self):
        self.assertEqual(Locus('name', sample_size = 23).to_leapdna(), 
            {'name': 'name', 'sample_size': 23, 'alleles': [] })

    def test_to_leapdna_returns_a_copy(self):
        l = Locus('lname')
        ldna = l.to_leapdna()
        ldna['name'] = 'other'

        self.assertEqual(ldna['name'], 'other')
        self.assertEqual(l.name, 'lname')

    def test_hexp(self):
        locus = Locus('name', alleles = [Allele('a', frequency = 0.5), Allele('b', frequency = 0.5)])
        self.assertEqual(locus.h_exp, 0.5)

    def test_sample_size(self):
        locus = Locus('name', alleles = [Allele('a', count = 10), Allele('b', count = 20)])
        self.assertEqual(locus.sample_size, 30)
        locus.sample_size = 123
        self.assertEqual(locus.sample_size, 123)