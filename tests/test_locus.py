import unittest

from leapdna.locus import Locus

class TestLocus(unittest.TestCase):
    def test_to_leapdna(self):
        self.assertEqual(Locus('name').to_leapdna(), {'name': 'name', 'alleles': []})
        self.assertEqual(Locus('name', [{'name':'a'}, {'name':'b'}]).to_leapdna(),
            {'name': 'name', 'alleles': [{'name':'a'}, {'name':'b'}]})

    def test_to_leapdna_returns_a_copy(self):
        l = Locus('lname')
        ldna = l.to_leapdna()
        ldna['name'] = 'other'

        self.assertEqual(ldna['name'], 'other')
        self.assertEqual(l.name, 'lname')