# "Evolueerder"

from tensorflow import *

from car import *
from road import *


class Selector:
    def __init__(self):
        self.road = self.make_road()
        self.cars = []

    def initial_generation(self):
        # Add 50 random cars
        self.cars = []
        for i in xrange(0, 50):
            car = Car()
            self.cars.append(car)

    def create_next_generation(self):
        # Select best performing cars
        best_performing = []
        for i in xrange(25):
            best_car_index = 0
            for c in range(0, len(self.cars)):
                if self.cars[c].collide_distance > self.cars[best_car_index].collide_distance:
                    best_car_index = c
            best_performing.append(self.cars.pop(best_car_index))

        # Create new generation with best_performing as parents
        new_generation = []
        for i in xrange(25):
            new_generation.append(Car(best_performing))

        # Add best_performing and new_generation to self.cars
        self.cars = []
        self.cars.append(car for car in best_performing)
        self.cars.append(car for car in new_generation)

    def test_generation(self):
        self.cars = self.road.test(self.cars)

    @staticmethod
    def make_road():
        new_road = Road()
        points = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
                  Point(300, 340), Point(150, 320), Point(50, 250)]
        new_road.set_road(points)
        return new_road
