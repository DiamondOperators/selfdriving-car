import random
from random import randint
import main


class Car(object):
    def __init__(self, parents=None, collide_distance=-1, direction=0, x=0, y=0):
        self.id = randint(0, 1000)
        self.x = float(x)
        self.y = float(y)
        self.speed = 1  # px per second
        self.direction = direction  # 0 = rechts, radialen
        self.collide_distance = collide_distance
        self.W1 = []
        self.W2 = []
        self.W3 = []  # weight3
        self.mutation_rate = .1
        self.checked = False

        # De range van de sensoren, in pixels; wordt gebruikt in road.get_sensor_data()
        self.sensor_range = 200

        if parents is not None:
            self.inherit_from(parents)
        else:
            self.random_weights()

    def inherit_from(self, parents):
        W11length = len(parents[0].W1)
        W12length = len(parents[0].W1[0])
        W21length = len(parents[0].W2)
        W22length = len(parents[0].W2[0])
        W31length = len(parents[0].W3)  # weight3
        W32length = len(parents[0].W3[0])  # weight3

        parent = random.choice(parents)

        self.W1 = []
        for i in range(W11length):
            w1i = []
            for j in range(W12length):
                value = parent.W1[i][j]
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
                value = parent.W2[i][j]
                mutation_chance = randint(1, 100)
                if mutation_chance <= 25:
                    perc = random.random() * self.mutation_rate * 2 - self.mutation_rate
                    value += perc * value
                w2i.append(value)
            self.W2.append(w2i)

        self.W3 = []  # weight3
        for i in range(W31length):
            w3i = []
            for j in range(W32length):
                value = parent.W3[i][j]
                mutation_chance = randint(1, 100)
                if mutation_chance <= 25:
                    perc = random.random() * self.mutation_rate * 2 - self.mutation_rate
                    value += perc * value
                w3i.append(value)
            self.W3.append(w3i)

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
            for j in range(main.ann.hiddenNodes2):
                w2i.append(random.random() * .05 - .025)
            self.W2.append(w2i)

        self.W3 = []  # weight3
        for i in range(main.ann.hiddenNodes2):
            w3i = []
            for j in range(main.ann.outputNodes):
                w3i.append(random.random() * .05 - .025)
            self.W3.append(w3i)

    def update_direction(self, sensor_data):
        self.direction += main.ann.propagate_forward(self, sensor_data)[0][0]

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def add_position(self, x, y):
        self.x += x
        self.y += y
