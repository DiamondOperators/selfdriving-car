# "Evolueerder"

from tensorflow import *
from road import *
from car import *


class Selector:
    def __init__(self):
        self.road = make_road()
        self.cars = []
        self.population_size = 4  # Uit hoeveel auto's een populatie bestaat; moet een even getal zijn

    def initial_generation(self):
        # Add {self.population_size} random cars
        self.cars = []
        for i in xrange(0, self.population_size):
            car = Car()
            self.cars.append(car)

    def create_next_generation(self):
        # Select best performing cars
        best_performing = []
        for i in xrange(self.population_size / 2):
            best_car_index = 0
            for c in range(0, len(self.cars)):
                if self.cars[c].collide_distance > self.cars[best_car_index].collide_distance:
                    best_car_index = c
            best_performing.append(self.cars.pop(best_car_index))

        # Create new generation with best_performing as parents
        new_generation = []
        for i in xrange(self.population_size / 2):
            new_generation.append(Car(best_performing))

        # Add best_performing and new_generation to self.cars
        self.cars = []
        self.cars.append(car for car in best_performing)
        self.cars.append(car for car in new_generation)

    def test_generation(self):
        self.cars = self.road.test(self.cars)


def make_road():
    new_road = Road()
    points = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
              Point(300, 340), Point(150, 320), Point(50, 250)]
    new_road.set_road(points, Point(300, 35))
    return new_road
