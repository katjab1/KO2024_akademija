import numpy as np
import math
class Individual:
    def __init__(self, numberOfTasks, l, p, r):
        self.passion = p
        self.perseverance = r
        self.learning = l
        self.overallSkill = []  # elements are skill levels of tasks
        self.overallChallenge = []  # elements are challenge levels of tasks
        self.numberOfTasks = numberOfTasks
        self.learningPeriod = 1000  # number of times we learn
        self.coefGSkill = -1
        self.coefGChallenge = 1
        self.coefGExpected = -1
        self.coefGOffset = 0.5
        self.coefFSkill = -1
        self.coefFExpected = -1
        self.coefFOffset = 0.5
        self.Hist_S = []
        self.Hist_C = []

        for i in range(numberOfTasks):
            self.overallSkill.append(np.random.uniform(0, 1))
            self.overallChallenge.append(np.random.uniform(0, 1))

    def probabilityFailure(self, index):
        if self.perseverance == 1:
            return 0
        elif self.perseverance == 0:
            return 1
        else:
            try:
                prob = 1 / (1 + math.exp((
                                                 -self.coefFSkill * self.overallSkill[index] -
                                                 self.coefFExpected * self.expectedAbility(index) +
                                                 self.coefFOffset) / (1 - self.perseverance)))
            except OverflowError:
                prob = float('inf')
            return prob

    def probabilityGiveUp(self, index):
        if self.perseverance == 1:
            return 0
        elif self.perseverance == 0:
            return 1
        else:
            try:
                prob = 1 / (1 + math.exp((
                                                 -self.coefGSkill * self.overallSkill[index] +
                                                 self.coefGChallenge * self.overallChallenge[index] -
                                                 self.coefGExpected * self.expectedAbility(index) +
                                                 self.coefGOffset) / (1 - self.perseverance)))
            except OverflowError:
                prob = float('inf')
            return prob

    def expectedAbility(self, index):
        # average of all skills of tasks except of task at given index
        res = 0
        for i in range(self.numberOfTasks):
            if (i == index):
                continue
            res += self.overallSkill[i]
        res = res / self.numberOfTasks
        return res

    def learn(self):
        for i in range(self.learningPeriod):
            index = np.random.randint(0, self.numberOfTasks)
            pf = self.probabilityFailure(index)
            pg = self.probabilityGiveUp(index)
            r = np.random.uniform(0, 1)

            if r < pg:
                self.give_up(index)
            else:
                r = np.random.uniform(0, 1)
                if r < pf:
                    self.failure(index)
                else:
                    self.success(index)

        s = []
        c = []
        for i in range(self.numberOfTasks):
            s.append(self.overallSkill[i])
            c.append(self.overallChallenge[i])

        return s, c

        # s: skills, c: challenges
        self.Hist_S.append(s)
        self.Hist_C.append(c)

    def give_up(self, index):
        self.overallChallenge[index] -= (1 - self.perseverance) * self.overallChallenge[index]
        self.overallSkill[index] += (self.learning * self.overallChallenge[index] *
                                     (1 - self.overallSkill[index])) * self.overallSkill[index] * np.random.uniform(0,
                                                                                                                    1)

    def failure(self, index):
        self.overallChallenge[index] -= (1 - self.perseverance) * self.overallChallenge[index]
        self.overallSkill[index] += (self.learning * self.overallChallenge[index] *
                                     (1 - self.overallSkill[index])) * self.overallSkill[index] * np.random.uniform(0,
                                                                                                                    1)

    def success(self, index):
        self.overallChallenge[index] += self.passion * (1 - self.overallChallenge[index]) * self.overallChallenge[index]
        self.overallSkill[index] += (self.learning * self.overallChallenge[index] *
                                     (1 - self.overallSkill[index])) * self.overallSkill[index]


    def average(self, field):
        res = 0
        for i in range(len(field)):
            res += field[i]
        res = res / len(field)
        return res



class Simulation:
    WORRY = 0
    ANXIETY = 1
    AROUSAL = 2
    FLOW = 3
    CONTROL = 4
    RELAXATION = 5
    BOREDOM = 6
    APATHY = 7
    UNDECIDED = 8

    cells = 9
    dSize = 1.0
    rCenter = 0.0005

    emoPhi = [7 * math.pi / 8, 5 * math.pi / 8, 3 * math.pi / 8, math.pi / 8, -math.pi / 8,
              -3 * math.pi / 8, -5 * math.pi / 8, -7 * math.pi / 8, math.pi / 8]

    def radius(self, x, y):
        x = x - self.dSize / 2
        y = y - self.dSize / 2
        return math.sqrt(x * x + y * y)

    def angle(self, x, y):
        x = x - self.dSize / 2
        y = y - self.dSize / 2
        return math.atan2(y, x)

    def emotionFromAngle(self, x, y):
        if self.radius(x, y) < self.rCenter:
            return self.UNDECIDED
        angle = self.angle(x, y)
        for i in range(self.cells - 1):
            if angle < self.emoPhi[i] and angle > self.emoPhi[i + 1]:
                return i + 1
        return 0

    def getState(self, l, r, p, num_Ind, number_Tasks):
        count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for ind in range(num_Ind):
            person = Individual(number_Tasks, l, p, r)
            a, b = person.learn()
            a1 = person.average(a)
            b1 = person.average(b)
            count[self.emotionFromAngle(a1, b1)] += 1
        em = count.index(max(count))
        percentage = float(max(count) / sum(count)) * 100
        print(str((em, percentage)))
        return (em, percentage)

"""
sim = Simulation()
for i in range(10):
    x = np.random.uniform(0, 1)
    y = np.random.uniform(0, 1)
    print("x: " + str(x) + " y: " + str(y))
    print(sim.emotionFromAngle(x, y))"""

person = Individual(10, 0.5, 0.5, 0.5)
l = np.random.random()  # Random number between 0 and 1
r = np.random.random()  # Random number between 0 and 1
p = np.random.random()  # Random number between 0 and 1
sim = Simulation()
print(person.overallSkill)
print(person.learn())
print(person.overallSkill)
#sim.getState(l,r,p,50,50)



