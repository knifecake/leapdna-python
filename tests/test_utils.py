import unittest

from leapdna.utils import *

class TestUtils(unittest.TestCase):
    def test_transpose(self):
        self.assertEqual(transpose([[1]]), [[1]])
        self.assertEqual(transpose([[1,2], [3,4]]), [[1,3], [2,4]])
        self.assertEqual(transpose([[1,2], [3,4], [5,6]]), [[1,3,5], [2,4,6]])
        self.assertEqual(transpose([[1,3,5], [2,4,6]]), [[1,2], [3,4], [5,6]])

    def test_union(self):
        self.assertEqual(union([]), set([]))
        self.assertEqual(union([1], []), set([1]))
        self.assertEqual(union([], [1]), set([1]))
        self.assertEqual(union([1,2], [2,3]), set([1,2,3]))
        self.assertEqual(union([1,2], [3,4]), set([1,2,3,4]))
        self.assertEqual(union([1,2], [1,2]), set([1,2]))