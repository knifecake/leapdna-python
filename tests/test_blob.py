from leapdna import blob
from leapdna.blocks.locus import Locus
from leapdna.errors import LeapdnaError
from leapdna import blocks
from leapdna.blocks.base import Base
from .support import TestCase

from leapdna.blob import LeapdnaBlob


class TestFromdict(TestCase):
    def test_can_be_instantiated(self):
        blob = LeapdnaBlob()
        self.assertTrue(blob is not None)

    def test_refuses_non_leapdna_data(self):
        data = {'bogus': 1}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob(data)

        data = {'block_type': 'locus', 'name': 'l1'}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob(data)

    def test_parse_block(self):
        data = {'block_type': 'locus', 'name': 'l1'}
        locus = LeapdnaBlob.parse_block(data)
        self.assertTrue(isinstance(locus, Locus))
        self.assertTrue(locus.name, 'l1')

    def test_parse_block_fails_for_non_leapdna_data(self):
        data = {'bogus': 1}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob.parse_block(data)

        data = {'incomplete': True}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob.parse_block(data)

        data = {'block_type': 'bogus', 'name': 'l1'}
        with self.assertRaises(LeapdnaError):
            LeapdnaBlob.parse_block(data)

    def test_generates_ids_for_blocks_without_id(self):
        block = Base()
        self.assertTrue(block.id is None)

        blob = LeapdnaBlob()
        initial_counter = blob.id_counter
        gen_id = blob.generate_id(block)

        self.assertEqual(gen_id, block.id)
        self.assertEqual(blob.id_counter, initial_counter + 1)

    def test_generates_ids_for_blocks_with_id(self):
        block = Base(id='my_id')
        self.assertTrue(block.id is not None)

        blob = LeapdnaBlob()
        initial_counter = blob.id_counter
        gen_id = blob.generate_id(block)
        self.assertEqual(gen_id, block.id)
        self.assertEqual(blob.id_counter, initial_counter)

    def test_cannot_append_non_leapdna_block(self):
        blob = LeapdnaBlob()
        with self.assertRaises(LeapdnaError):
            blob.append(1)

    def test_autogenerates_ids_for_blocks(self):
        blob = LeapdnaBlob()
        block = Base()
        self.assertTrue(block.id is None)
        blob.append(block)
        self.assertFalse(block.id is None)

    def test_cannot_append_different_blocks_with_same_id(self):
        blob = LeapdnaBlob()
        b1 = Base(id='123')
        b2 = Locus(name='123')
        with self.assertRaises(LeapdnaError):
            blob.append(b1)
            blob.append(b2)