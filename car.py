import random

import main


class Car(object):
    def __init__(self, parents=None, collide_distance=-1, direction=0, x=0, y=0):
        self.x = x
        self.y = y
        self.speed = 1  # px per second
        self.direction = direction  # 0 = rechts, radialen
        self.collide_distance = collide_distance
        self.W1 = []
        self.W2 = []

        if parents is not None:
            self.inherit_from(parents)
        else:
            self.random_weights()

    def inherit_from(self, parents):
        self.W1 = []
        for i in range(main.ann.inputNodes):
            w1i = []
            for j in range(main.ann.hiddenNodes):
                parent = parents[random.randint(0, len(parents))]
                w1i.append(parent.W1[i][j])
            self.W1.append(w1i)

        self.W2 = []
        for i in range(main.ann.hiddenNodes):
            w2i = []
            for j in range(main.ann.outputNodes):
                parent = parents[random.randint(0, len(parents))]
                w2i.append(parent.W2[i][j])
            self.W2.append(w2i)

    def random_weights(self):
        pass

    def update_direction(self, sensor_data):
        self.direction += main.ann.propagate_forward(self, sensor_data)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def add_position(self, x, y):
        self.x += x
        self.y += y
