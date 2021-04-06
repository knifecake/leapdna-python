from .support import TestCase

from leapdna.blocks import Base, Locus


class TestBaseBlock(TestCase):
    def test_can_be_instantiated_from_a_dict(self):
        data = {'block_type': 'base', 'id': 1234, 'user': {'custom_prop': 123}}

        res = Base(**data)
        self.assertEqual(res.block_type, 'base')
        self.assertEqual(res.id, 1234)
        self.assertEqual(res.user['custom_prop'], 123)

    def test_can_be_converted_to_dict(self):
        data = {
            'block_type': 'base',
            'id': '1234',
            'user': {
                'custom_prop': 123
            }
        }
        block = Base(**data)
        self.assertEqual(data, block.asdict())

    def test_has_string_representation(self):
        block = Base(id='123')
        self.assertIn('123', str(block))
        self.assertIn('123', repr(block))

    def test_equality(self):
        b1 = Base(id='123')
        b2 = Base(id='123')
        self.assertEqual(b1, b2)

        b2 = Locus(name='123')
        self.assertNotEqual(b1, b2)