from ANN import *


class Car(object):
    def __init__(self, ann=None, parents=None, collide_distance=-1, direction=0, x=0, y=0):
        self.x = x
        self.y = y
        self.speed = 1  # px per second
        self.direction = direction  # 0 = rechts, radialen
        self.collide_distance = collide_distance

        if ann is None:
            if parents is None or len(parents) == 0:
                self.ann = ANN()
            else:
                self.inherit_from(parents)
        else:
            self.ann = ann

    def inherit_from(self, parents):
        pass

    def update_direction(self, sensor_data):
        self.direction += self.ann.propagate_forward(sensor_data)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def add_position(self, x, y):
        self.x += x
        self.y += y
