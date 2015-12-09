class Car(object):
    def __init__(self, x, y, ann):
        self.x = x
        self.y = y
        self.speed = 1  # px per second
        self.direction = 0  # 0 = rechts, radialen
        self.ann = ann
        self.collide_distance = -1

    def update_direction(self, sensor_data):
        self.direction += self.ann.propagate_forward(sensor_data)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def add_position(self, x, y):
        self.x += x
        self.y += y
