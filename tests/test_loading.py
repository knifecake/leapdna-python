from leapdna.errors import LeapdnaError
from leapdna.blocks.allele import Allele
from leapdna.blocks.base import Base
from .support import TestCase

from leapdna.blob import LeapdnaBlob


class TestFromdict(TestCase):
    def test_loads_single_base_block(self):
        data = {'block_type': 'base', 'id': 1234, 'user': {'custom_prop': 123}}

        res = LeapdnaBlob.parse_block(data)
        self.assertTrue(isinstance(res, Base))
        self.assertEqual(res.user['custom_prop'], 123)

    def test_loads_blob_with_blob_ids(self):
        """Tests that objects in blobs get the id of the key in which they are stored
        in the blob, even if it is different from the one specified in the 'leapdna'
        part of the block."""
        data = {'block_type': 'blob', 'b1': {'block_type': 'base'}}
        res = LeapdnaBlob(data)
        self.assertIn('b1', res)
        self.assertEqual(res['b1'].id, 'b1')

    def test_loads_blob_with_allele(self):
        data = {
            'block_type': 'blob',
            'a1': {
                'name': 'a1',
                'locus': 'l1',
                'block_type': 'allele'
            }
        }
        res = LeapdnaBlob(data)
        self.assertTrue(isinstance(res['a1'], Allele))
        self.assertEqual(res['a1'].name, 'a1')

    def test_loads_blob_with_allele_and_locus(self):
        data = {
            'block_type': 'blob',
            'a1': {
                'name': 'a1',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'a2': {
                'name': 'a2',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'l1': {
                'name': 'l1',
                'block_type': 'locus'
            }
        }
        res = LeapdnaBlob(data)
        self.assertEqual(res['a1'].locus, res['l1'])

    def test_loads_blob_with_observation(self):
        data = {
            'block_type': 'blob',
            'a1': {
                'name': 'a1',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'a2': {
                'name': 'a2',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'l1': {
                'name': 'l1',
                'block_type': 'locus'
            },
            'o1': {
                'allele': 'a1',
                'count': 10,
                'block_type': 'observation'
            },
            'o2': {
                'allele': 'a2',
                'count': 90,
                'block_type': 'observation'
            }
        }
        res = LeapdnaBlob(data)
        self.assertEqual(res['o1'].locus, res['l1'])
        self.assertEqual(res['o1'].allele, res['a1'])

    def test_loads_blob_with_observation_summary(self):
        data = {
            'block_type': 'blob',
            'a1': {
                'name': 'a1',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'a2': {
                'name': 'a2',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'l1': {
                'name': 'l1',
                'block_type': 'locus'
            },
            'o1': {
                'allele': 'a1',
                'count': 23,
                'block_type': 'observation'
            }
        }
        res = LeapdnaBlob(data)
        self.assertEqual(res['o1'].locus, res['l1'])
        self.assertEqual(res['o1'].allele, res['a1'])
        self.assertEqual(res['o1'].count, 23)

    def test_loads_study(self):
        data = {
            'block_type': 'blob',
            'a1': {
                'name': 'a1',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'a2': {
                'name': 'a2',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'l1': {
                'name': 'l1',
                'block_type': 'locus'
            },
            'o1': {
                'allele': 'a1',
                'count': 10,
                'block_type': 'observation'
            },
            'o2': {
                'allele': 'a2',
                'count': 90,
                'block_type': 'observation'
            },
            's1': {
                'observations': ['o1', 'o2'],
                'block_type': 'study'
            }
        }

        res = LeapdnaBlob(data)
        self.assertEqual(res['o1'].locus, res['l1'])
        self.assertEqual(res['o1'].allele, res['a1'])

    def test_studies_need_full_resolution(self):
        data = {
            'block_type': 'blob',
            'a1': {
                'name': 'a1',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'a2': {
                'name': 'a2',
                'locus': 'l1',
                'block_type': 'allele'
            },
            'l1': {
                'name': 'l1',
                'block_type': 'locus'
            },
            'o1': {
                'allele': 'a1',
                'count': 10,
                'block_type': 'observation'
            },
            'o2': {
                'allele': 'a2',
                'count': 90,
                'block_type': 'observation'
            },
            's1': {
                'observations': ['o1', 'o2', 'o3'],
                'block_type': 'study'
            }
        }

        with self.assertRaises(LeapdnaError):
            LeapdnaBlob(data)