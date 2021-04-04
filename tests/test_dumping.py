from leapdna.blob import LeapdnaBlob
from .support import TestCase
from leapdna.blocks import Locus, Allele, Observation, Study


class TestDumping(TestCase):
    def test_dumps_alleles_and_loci(self):
        l1 = Locus('l1')
        a1 = Allele('a1', l1)
        a2 = Allele('a2', l1)
        study = Study([
            Observation(a1, frequency=0.25, id='o1'),
            Observation(a2, frequency=0.75, id='o2')
        ],
                      id='study_id')

        blob = LeapdnaBlob()
        blob.append(study)

        res = blob.asdict()
        self.assertCountEqual(
            res.keys(), ['leapdna', 'l1', 'a1', 'a2', 'o1', 'o2', 'study_id'])
