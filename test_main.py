import math
from unittest import TestCase
from main import Individual, Simulation
import random


class TestIndividual(TestCase):
    def test_probability_give_up(self):
        for i in range(100000):
            if i % 10000 == 0:
                print(i)
            r = random.random()
            per = Individual(numberOfTasks=10, l=0.5, p=0.5, r=r)
            print(r)
            per.probabilityGiveUp(1)


class TestIndividual(TestCase):
    def test_probability_failure(self):
        for i in range(100000):
            if i % 10000 == 0:
                print(i)
            r = random.random()
            per = Individual(numberOfTasks=10, l=0.5, p=0.5, r=r)
            print(r)
            per.probabilityFailure(1)


class TestSimulation(TestCase):
    def test_radius(self):
        sim = Simulation()
        sim.dSize = 1.0
        sim.rCenter = 0.005

        self.assertEqual(sim.radius(0.5, 0.5), 0)
        self.assertAlmostEqual(sim.radius(0, 0), 0.7071067812)
        self.assertAlmostEqual(sim.radius(1, 1), 0.7071067812)
        self.assertAlmostEqual(sim.radius(0.2, 0.3), 0.360555127546)


class TestSimulation(TestCase):
    def test_angle(self):
        sim = Simulation()
        sim.dSize = 1.0
        sim.rCenter = 0.005

        self.assertEqual(sim.angle(0.5, 0.5), 0)
        self.assertEqual(sim.angle(1.5, 0.5), 0)
        self.assertEqual(sim.angle(0.5, 1.5), math.pi / 2)


class TestSimulation(TestCase):
    def test_emotion_from_angle(self):
        sim = Simulation()
        sim.dSize = 1.0
        sim.rCenter = 0.005

        self.assertEqual(sim.emotionFromAngle(0.5, 0.5), sim.UNDECIDED)
        self.assertEqual(sim.emotionFromAngle(0.5, 1), sim.AROUSAL)
        self.assertEqual(sim.emotionFromAngle(0, 0.5), sim.WORRY)
        self.assertEqual(sim.emotionFromAngle(0, 1), sim.ANXIETY)
        self.assertEqual(sim.emotionFromAngle(0.5, 0), sim.BOREDOM)
        self.assertEqual(sim.emotionFromAngle(0.2, 0.2), sim.APATHY)
        self.assertEqual(sim.emotionFromAngle(1, 0), sim.RELAXATION)
        self.assertEqual(sim.emotionFromAngle(1, 0.5), sim.CONTROL)
        self.assertEqual(sim.emotionFromAngle(1, 1), sim.FLOW)


class TestSimulation(TestCase):
    def test_get_state(self):
        sim = Simulation()
        sim.dSize = 1.0
        sim.rCenter = 0.005
        self.assertEqual(sim.getState(0,0,0,10,50), (sim.WORRY,100))
