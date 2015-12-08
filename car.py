class Car(object):
    def __init__(self, x, y, ann):
        self.x = x
        self.y = y
        self.speed = 50  # px per second
        self.direction = 0  # 0 = rechts, radialen
        self.ann = ann

    def update_direction(self, sensor_data):
        self.direction = self.ann.adjust_direction(sensor_data)

    def set_position(self, x, y):
        self.x = x
        self.y = y
