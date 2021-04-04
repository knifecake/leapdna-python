from .support import TestCase

from leapdna.blocks import Base, Locus, Allele, Observation, Study, observation


class TestDeps(TestCase):
    def test_base_block_deps(self):
        base = Base()
        self.assertEqual(base.block_deps(), {})

    def test_locus_block_deps(self):
        locus = Locus('l1')
        self.assertEqual(locus.block_deps(), {})

    def test_allele_block_deps(self):
        locus = Locus('l1')
        allele = Allele('a1', locus)
        self.assertEqual(allele.block_deps(), {locus.id: locus})

    def test_observation_block_deps(self):
        locus = Locus('l1')
        allele = Allele('a1', locus)
        observation = Observation(allele=allele)

        self.assertEqual(observation.block_deps(), {
            allele.id: allele,
            locus.id: locus
        })

    def test_study_block_deps(self):
        locus = Locus('l1')
        allele = Allele('a1', locus)
        observation = Observation(allele=allele, frequency=0.15)
        study = Study([observation])

        self.assertEqual(study.block_deps(), {
            observation.id: observation,
            allele.id: allele,
            locus.id: locus
        })
