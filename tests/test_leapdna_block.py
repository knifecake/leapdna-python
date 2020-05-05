import unittest

from leapdna.block import LeapdnaBlock

class TestLeapdnaBlock(unittest.TestCase):
    def test_to_leapdna(self):
        b = LeapdnaBlock(id = 'myid')
        self.assertNotIn('version', b.to_leapdna())
        self.assertEqual(b.to_leapdna()['id'], 'myid')

    def test_to_leapdna_top_level(self):
        b = LeapdnaBlock(version = 1)
        self.assertEqual(b.to_leapdna(top_level = True)['version'], 1)

    def test_user_params_are_serialized(self):
        b = LeapdnaBlock(custom = 'value')
        self.assertEqual(b.to_leapdna()['user']['custom'], 'value')

