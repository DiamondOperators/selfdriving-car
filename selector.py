# "Evolueerder"

from road import *
from car import *


class Selector:
    def __init__(self):
        self.road = make_road()
        self.cars = []
        self.population_size = 10  # Uit hoeveel auto's een populatie bestaat; moet een even getal zijn

    def initial_generation(self):
        # Add {self.population_size} random cars
        self.cars = []
        for i in xrange(0, self.population_size):
            self.cars.append(Car())

    def create_next_generation(self):
        # Sort cars by collide_distance descending
        # Uses bubblesort algorithm
        for h in xrange(1, len(self.cars) - 1):
            i = len(self.cars) - h  # i gaat dus van len(self.cars) naar (en inclusief) 2
            for j in xrange(0, i):
                if self.cars[j].collide_distance < self.cars[j + 1].collide_distance:
                    temp = self.cars[j]
                    self.cars[j] = self.cars[j + 1]
                    self.cars[j + 1] = temp

        # The best 25 cars are now in the first 25 indices of the array.
        # Substitute the last 25 cars in the array with new ones.
        for i in xrange(len(self.cars) / 2, len(self.cars)):
            self.cars[i] = Car(self.cars, len(self.cars) / 2)

    def test_generation(self):
        self.cars = self.road.test(self.cars)


def make_road():
    new_road = Road()
    points = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
              Point(300, 340), Point(150, 320), Point(50, 250)]
    new_road.set_road(points, Point(400, 55))
    return new_road
