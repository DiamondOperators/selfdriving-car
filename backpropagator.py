from road import *
from backpropcar import *
import roadmaker
from graphics import *
import random

train_interval = 5
train_chance = 20


class Backpropagator:
    def __init__(self):
        self.car = BackpropCar()
        self.road = roadmaker.fetch_road()

        while 1 + 1 == 2:
            self.reset_car()
            self.train2()

    def reset_car(self):
        self.car.direction = self.road.starting_direction
        self.car.x = self.road.start.x
        self.car.y = self.road.start.y

    def train2(self):
        sensor_inputs = []
        proper_outputs = []

        while 1 + 1 == 2:
            sensor_data = self.road.get_sensor_data(self.car)

            if random.randint(1, train_interval) == train_interval:
                # Chance of one in {train_interval} that this code is executed
                sensor_inputs.append(sensor_data[0])
                desired_direction_change = self.road.desired_direction(self.car) - self.car.direction
                proper_outputs.append([desired_direction_change])  # proper_outputs has to be a 2D array

            self.car.update_direction(self.road.get_sensor_data(self.car))
            x_diff = math.cos(self.car.direction)
            y_diff = math.sin(self.car.direction)
            self.car.x += x_diff
            self.car.y += y_diff

            if self.road.car_collided(self.car):
                self.car.collide_distance = self.road.collide_distance(self.car)
                print "\nCollide distance:", self.car.collide_distance, "\n"
                break

            self.road.redraw()
            Point(self.car.x, self.car.y).draw(self.road.win)

        # The car has collided; train it using the collected data
        self.car.train(sensor_inputs, proper_outputs)

    def train(self):
        step = 0

        while not self.road.car_collided(self.car):
            if step % train_interval == 0:
                desired_direction = self.road.desired_direction(self.car)
                desired_direction_change = desired_direction - self.car.direction

                self.car.train(self.road.get_sensor_data(self.car), [[desired_direction_change]])

            self.car.update_direction(self.road.get_sensor_data(self.car))

            x_diff = math.cos(self.car.direction)
            y_diff = math.sin(self.car.direction)
            self.car.x += x_diff
            self.car.y += y_diff

            if self.road.car_collided(self.car):
                self.car.collide_distance = self.road.collide_distance(self.car)
                print "\nCollide distance:", self.car.collide_distance, "\n"

            # if self.road.point_collides_with_line(self.road.back_check, car.x, car.y):
            #     self.car.checked = True
            self.road.redraw()
            Point(self.car.x, self.car.y).draw(self.road.win)

            step += 1
