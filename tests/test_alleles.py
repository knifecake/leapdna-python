import unittest
import csv

from leapdna.allele import repeat_to_seq
from leapdna.utils import transpose

class TestAlleles(unittest.TestCase):
    def test_repeat_to_seq(self):
        self.assertEqual(repeat_to_seq(''), '')
        self.assertEqual(repeat_to_seq('ABCD'), 'ABCD')
        self.assertEqual(repeat_to_seq('[A]2'), 'AA')
        self.assertEqual(repeat_to_seq('[A]3B'), 'AAAB')
        self.assertEqual(repeat_to_seq('[A]2[B]2'), 'AABB')
        self.assertEqual(repeat_to_seq('[A]10'), 'A' * 10)
        self.assertEqual(repeat_to_seq('A[B]2'), 'ABB')

    def test_repeat_to_seq_fga_data(self):
        with open('tests/stubs/repeat_to_seq_FGA.csv', newline = '') as f:
            data = list(csv.reader(f, delimiter = ';'))
            for repeat, seq in data:
                self.assertEqual(repeat_to_seq(repeat), seq,
                    msg = f'Failed in repeat {repeat}')
            