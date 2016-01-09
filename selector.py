# "Evolueerder"

from road import *
from car import *
import roadmaker


class Selector:
    def __init__(self):
        self.road = roadmaker.parse_road(raw_input("What road? "))
        self.cars = []
        self.population_size = 12  # Uit hoeveel auto's een populatie bestaat; moet een even getal zijn

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

        stay_alive = int(len(self.cars) * .2)
        parents = []
        for i in range(0, stay_alive):
            parents.append(self.cars[i])

        # The best 25 cars are now in the first 25 indices of the array.
        # Substitute the last 25 cars in the array with new ones.
        for i in xrange(stay_alive, len(self.cars)):
            self.cars[i] = Car(parents)

    def test_generation(self):
        for car in self.cars:
            car.collide_distance = -1

        self.cars = self.road.test(self.cars)


def make_road():
    new_road = Road()
    points = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
              Point(300, 340), Point(150, 320), Point(50, 250)]
    check_line = Line(Point(140, 100), Point(140, 10))
    new_road.set_road(points, Point(100, 70), check_line)
    return new_road
