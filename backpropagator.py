from road import *
from car import *
import roadmaker
import tensorflow


class Backpropagator:
    def __init__(self):
        self.car = Car()
        self.start()

    def start(self):
        while 1 + 1 == 2:
            self.train()

    def train(self):
        self.car.set_position(main.road.finish.x, main.road.finish.y)

        train_interval = 10
        step = 0

        while not main.road.car_collided(self.car):
            if step % train_interval == 0:
                # Train
                pass

            car.update_direction(self.get_sensor_data(car))

            x_diff = math.cos(car.direction) * car.speed
            y_diff = math.sin(car.direction) * car.speed
            car.add_position(x_diff, y_diff)

            if self.car_collided(car):
                car.collide_distance = self.collide_distance(car)

            if self.point_collides_with_line(self.back_check, car.x, car.y):
                car.checked = True
            main.road.redraw()

            step += 1
