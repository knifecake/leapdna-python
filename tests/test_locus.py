import unittest

from leapdna.locus import Locus
from leapdna.allele import Allele

class TestLocus(unittest.TestCase):
    def test_to_leapdna(self):
        self.assertEqual(Locus('name').to_leapdna(), {'name': 'name', 'alleles': [], 'type': 'locus'})
        self.assertEqual(Locus('name', [{'name':'a'}, {'name':'b'}]).to_leapdna(),
                         {'name': 'name', 'type': 'locus', 'alleles': [{'name':'a', 'type': 'allele'}, {'name':'b', 'type': 'allele' }]})

    def test_to_leapdna_moves_dprops_to_top_level(self):
        self.assertEqual(Locus('name', sample_size = 23).to_leapdna(), 
            {'name': 'name', 'sample_size': 23, 'alleles': [], 'type': 'locus' })

    def test_to_leapdna_returns_a_copy(self):
        l = Locus('lname')
        ldna = l.to_leapdna()
        ldna['name'] = 'other'

        self.assertEqual(ldna['name'], 'other')
        self.assertEqual(l.name, 'lname')

    def test_hobs(self):
        locus = Locus('name', h_obs = 0.4, alleles = [Allele('a', frequency = 0.5), Allele('b', frequency = 0.5)])
        self.assertEqual(locus.h_obs, 0.4)
        locus.h_obs = 0.6
        self.assertEqual(locus.h_obs, 0.6)

    def test_set_hobs(self):
        with self.assertRaises(AssertionError):
            l = Locus('name')
            l.h_obs = 1.2

        with self.assertRaises(AssertionError):
            l = Locus('name', h_obs = 1.2)

    def test_hexp(self):
        locus = Locus('name', alleles = [Allele('a', frequency = 0.5), Allele('b', frequency = 0.5)])
        self.assertEqual(locus.h_exp, 0.5)

    def test_set_hexp(self):
        locus = Locus('name', alleles = [Allele('a', frequency = 0.5), Allele('b', frequency = 0.5)])
        with self.assertRaises(AssertionError):
            locus.h_exp = 12

    def test_sample_size(self):
        locus = Locus('name', alleles = [Allele('a', count = 10), Allele('b', count = 20)])
        self.assertEqual(locus.sample_size, 30)
        locus.sample_size = 123
        self.assertEqual(locus.sample_size, 123)

    def test_sample_size_fails(self):
        locus = Locus('name', alleles = [Allele('a', count = 10), Allele('b')])
        with self.assertRaises(ValueError):
            locus.sample_size

    def test_calculates_total_sample_size(self):
        locus = Locus('name', alleles = [
            Allele('a', count = 10),
            Allele('b', count = 20)
        ])

        self.assertEqual(locus._sample_size_sum(), 30)

    def test_calculates_total_frequencies(self):
        locus = Locus('name', alleles = [
            Allele('a', frequency = 0.25),
            Allele('b', frequency = 0.25)
        ])

        self.assertEqual(locus._allele_frequency_sum(), 0.5)
