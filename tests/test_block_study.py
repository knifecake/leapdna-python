from leapdna.blocks.observation import Observation
from .support import TestCase
from leapdna.blocks import Study, Locus, Allele


class TestStudyBlock(TestCase):
    def test_can_be_instantiated(self):
        l1 = Locus('l1')
        a1 = Allele('a1', l1)
        a2 = Allele('a2', l1)
        l2 = Locus('l2')
        a3 = Allele('a3', l2)
        a4 = Allele('a4', l2)

        study = Study([
            Observation(a1, count=50),
            Observation(a2, count=50),
            Observation(a3, count=10),
            Observation(a4, count=90)
        ])
        study.calculate_frequencies()
        self.assertTrue(study is not None)
        self.assertEqual(study.get_freq(a1), 0.5)
        self.assertEqual(study.get_freq(a3), 0.1)
        self.assertEqual(study.get_freq(Allele('new', l1)), 0)
        self.assertEqual(study.get_freq_by_names('l1', 'a1'), 0.5)
        self.assertEqual(study.get_freq_by_names('l3', 'a5'), 0)

        # force index rebuild
        study.allele_index = None
        self.assertEqual(study.get_freq(a3), 0.1)

        self.assertCountEqual(study.loci, [l1, l2])