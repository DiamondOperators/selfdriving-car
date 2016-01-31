from road import *
import road
from backpropcar import *
import roadmaker

train_interval = 10


class Backpropagator:
    def __init__(self):
        self.car = BackpropCar()
        self.road = roadmaker.fetch_road()

        while 1 + 1 == 2:
            self.reset_car()
            self.train()

    def reset_car(self):
        self.car.direction = self.road.starting_direction
        self.car.x = self.road.start.x
        self.car.y = self.road.start.y

    def train(self):
        step = 0

        while not self.road.car_collided(self.car):
            if step % train_interval == 0 and step != 0:
                distances = []
                for line in self.road.distance_check:
                    distances.append(road.distance_to_line_segment(line, self.car))
                current_segment = self.road.distance_check[distances.index(min(distances))]

                desired_direction = math.atan2(float(current_segment.p2.y) - float(self.car.y),
                                               float(current_segment.p2.x) - float(self.car.x))
                desired_direction_change = desired_direction - self.car.direction

                self.car.train(self.road.get_sensor_data(self.car), [[desired_direction_change]])

            self.car.update_direction(self.road.get_sensor_data(self.car))

            x_diff = math.cos(self.car.direction) * self.car.speed
            y_diff = math.sin(self.car.direction) * self.car.speed
            self.car.x += x_diff
            self.car.y += y_diff

            if self.road.car_collided(self.car):
                self.car.collide_distance = self.road.collide_distance(self.car)
                print "Collide distance:", self.car.collide_distance

            # if self.road.point_collides_with_line(self.road.back_check, car.x, car.y):
            #     self.car.checked = True
            self.road.redraw()

            step += 1
