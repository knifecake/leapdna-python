from .support import TestCase

from leapdna.blocks import Base, Locus, Allele, Observation, Study, observation


class TestAsdict(TestCase):
    def test_base_block_asdict(self):
        block = Base(id='id1', user={'field': 'value'})
        d = block.asdict()

        self.assertEqual(d['leapdna']['id'], 'id1')
        self.assertEqual(d['leapdna']['block_type'], 'base')
        self.assertEqual(d['user']['field'], 'value')

    def test_locus_block_asdict(self):
        locus = Locus(name='l1',
                      coords=('X', 10, 30),
                      band='test_band',
                      id='l1',
                      user={'field': 'value'})
        d = locus.asdict()
        self.assertEqual(d['leapdna']['id'], 'l1')
        self.assertEqual(d['leapdna']['block_type'], 'locus')
        self.assertEqual(d['name'], 'l1')
        self.assertEqual(d['band'], 'test_band')
        self.assertEqual(d['coords'], ('X', 10, 30))
        self.assertEqual(d['user']['field'], 'value')

    def test_allele_block_asdict(self):
        l1 = Locus(name='l1')
        allele = Allele(name='a1', locus=l1, id='a1')
        d = allele.asdict()

        self.assertEqual(d['leapdna']['id'], 'a1')
        self.assertEqual(d['leapdna']['block_type'], 'allele')
        self.assertEqual(d['name'], 'a1')
        self.assertEqual(d['locus'], 'l1')

        d = allele.asdict(without_deps=True)
        self.assertEqual(d['leapdna']['id'], 'a1')
        self.assertEqual(d['leapdna']['block_type'], 'allele')
        self.assertEqual(d['name'], 'a1')
        self.assertEqual(d['locus'], l1.asdict(without_deps=True))

    def test_observation_block_asdict(self):
        l1 = Locus(name='l1')
        a1 = Allele(name='a1', locus=l1, id='a1')
        observation = Observation(a1, count=10, frequency=0.1)

        d = observation.asdict()
        self.assertEqual(d['leapdna']['id'], 'observation_a1')
        self.assertEqual(d['leapdna']['block_type'], 'observation')
        self.assertEqual(d['allele'], 'a1')
        self.assertEqual(d['count'], 10)
        self.assertEqual(d['frequency'], 0.1)

        d = observation.asdict(without_deps=True)
        self.assertEqual(d['leapdna']['id'], 'observation_a1')
        self.assertEqual(d['leapdna']['block_type'], 'observation')
        self.assertEqual(d['allele'], a1.asdict(without_deps=True))

    def test_study_block_asdict(self):
        l1 = Locus(name='l1')
        a1 = Allele(name='a1', locus=l1, id='a1')
        o1 = Observation(a1, count=10, frequency=0.1, id='o1')
        study = Study(observations=[o1], id='s1')

        d = study.asdict()
        self.assertEqual(d['leapdna']['id'], 's1')
        self.assertEqual(d['leapdna']['block_type'], 'study')
        self.assertEqual(d['observations'], ['o1'])

        d = study.asdict(without_deps=True)
        self.assertEqual(d['leapdna']['id'], 's1')
        self.assertEqual(d['leapdna']['block_type'], 'study')
        self.assertEqual(d['observations'], [o1.asdict(without_deps=True)])
