from leapdna.blob import LeapdnaBlob
from .support import TestCase
from leapdna.blocks import Locus, Allele, Observation, Study


class TestDumping(TestCase):
    def test_dumps_alleles_and_loci(self):
        l1 = Locus('l1')
        a1 = Allele('a1', l1)
        a2 = Allele('a2', l1)
        study = Study(
            [Observation(a1, frequency=0.25),
             Observation(a2, frequency=0.75)],
            id='st1')
        study.prefix_observation_ids()

        blob = LeapdnaBlob()
        blob.append(study)
        res = blob.asdict()
        self.assertCountEqual(res.keys(), [
            'l1', 'a1@l1', 'a2@l1', 'st1_obs_a1@l1', 'st1_obs_a2@l1', 'st1',
            'block_type'
        ])
