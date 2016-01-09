import random
from random import randint
import main
import math


class Car(object):
    def __init__(self, parents=None, collide_distance=-1, direction=0, x=0, y=0):
        self.x = float(x)
        self.y = float(y)
        self.speed = 1  # px per second
        self.direction = direction  # 0 = rechts, radialen
        self.collide_distance = collide_distance
        self.W1 = []
        self.W2 = []
        self.mutation_rate = .1
        self.checked = False

        # De range van de sensoren, in pixels; wordt gebruikt in road.get_sensor_data()
        self.sensor_range = 50

        if parents is not None:
            self.inherit_from(parents)
        else:
            self.random_weights()

    def inherit_from(self, parents):
        W11length = len(parents[0].W1)
        W12length = len(parents[0].W1[0])
        W21length = len(parents[0].W2)
        W22length = len(parents[0].W2[0])

        self.W1 = []
        for i in range(W11length):
            w1i = []
            for j in range(W12length):
                value = random.choice(parents).W1[i][j]
                mutation_chance = randint(1, 100)
                if mutation_chance <= 25:
                    perc = random.random() * self.mutation_rate * 2 - self.mutation_rate
                    value += perc * value
                    w1i.append(value)
            self.W1.append(w1i)

        self.W2 = []
        for i in range(W21length):
            w2i = []
            for j in range(W22length):
                value = random.choice(parents).W2[i][j]
                mutation_chance = randint(1, 100)
                if mutation_chance <= 25:
                    perc = random.random() * self.mutation_rate * 2 - self.mutation_rate
                    value += perc * value
                    w2i.append(value)
            self.W2.append(w2i)

    def random_weights(self):
        self.W1 = []
        for i in range(main.ann.inputNodes):
            w1i = []
            for j in range(main.ann.hiddenNodes):
                w1i.append(random.random() * .05 - .025)
            self.W1.append(w1i)

        self.W2 = []
        for i in range(main.ann.hiddenNodes):
            w2i = []
            for j in range(main.ann.outputNodes):
                w2i.append(random.random() * .05 - .025)
            self.W2.append(w2i)

    def update_direction(self, sensor_data):
        self.direction += main.ann.propagate_forward(self, sensor_data)[0][0] * math.pi / 2

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def add_position(self, x, y):
        self.x += x
        self.y += y
