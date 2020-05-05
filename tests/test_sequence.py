import unittest
import csv

from leapdna.sequence import Sequence

class TestSequence(unittest.TestCase):
    def test_cannot_create_sequence_with_wrong_type(self):
        with self.assertRaises(AssertionError):
            Sequence(**{'type': 'allele'})

    def test_empty_to_leapdna(self):
        sq = Sequence()
        expected = {
            'type': 'sequence',
        }
        self.assertEqual(sq.to_leapdna(), expected)

    def test_to_leapdna(self):
        sq = Sequence(flank5_bracketed = '[ATTC]2')
        self.assertEqual(sq.to_leapdna()['flank5_bracketed'], '[ATTC]2')
    
    def test_returns_name(self):
        sq = Sequence(name = 'myname')
        self.assertEqual(sq.name, 'myname')

    def test_computes_sequences_from_bracketed(self):
        sq = Sequence(repeating_bracketed = '[ATTC]2')
        self.assertEqual(sq.repeating_seq, 'ATTCATTC')

    def test_repeat_to_seq(self):
        self.assertEqual(Sequence.bracketed_to_seq(''), '')
        self.assertEqual(Sequence.bracketed_to_seq('ABCD'), 'ABCD')
        self.assertEqual(Sequence.bracketed_to_seq('[A]2'), 'AA')
        self.assertEqual(Sequence.bracketed_to_seq('[A]3B'), 'AAAB')
        self.assertEqual(Sequence.bracketed_to_seq('[A]2[B]2'), 'AABB')
        self.assertEqual(Sequence.bracketed_to_seq('[A]10'), 'A' * 10)
        self.assertEqual(Sequence.bracketed_to_seq('A[B]2'), 'ABB')

    def test_repeat_to_seq_fga_data(self):
        with open('tests/stubs/repeat_to_seq_FGA.csv', newline = '') as f:
            data = list(csv.reader(f, delimiter = ';'))
            for repeat, seq in data:
                self.assertEqual(Sequence.bracketed_to_seq(repeat), seq,
                    msg = f'Failed in repeat {repeat}')
