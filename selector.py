# "Evolueerder"

from road import *
from car import *
import roadmaker
import time


class Selector:
    def __init__(self):
        self.road = roadmaker.fetch_road()
        self.cars = []
        self.population_size = 14  # Has to be an even number
        self.max_fitness = 0
        self.avg_fitness = 0
        self.generation = 0

    def initial_generation(self):
        # Add {self.population_size} random cars
        self.cars = []
        for i in xrange(0, self.population_size):
            self.cars.append(Car())

    def create_next_generation(self):
        stay_alive = int(len(self.cars) * .5)
        parents = []
        for i in range(0, stay_alive):
            parents.append(self.cars[i])

        # The best 10 cars are now in the first 10 indices of the array.
        # Substitute the last 10 cars in the array with new ones.
        for i in xrange(stay_alive, len(self.cars)):
            self.cars[i] = Car(parents)

    def start(self):
        self.initial_generation()
        self.generation = 0
        self.test_generation()

        while 1 + 1 == 2:
            self.generation += 1
            self.road.reset_win()
            self.create_next_generation()
            if self.test_generation():
                break

    def test_generation(self):
        try:
            self.road.test(self.cars)
        except KeyboardInterrupt:
            pass

        # Sort the cars by collide_distance descending
        # Uses bubblesort algorithm
        for h in xrange(1, len(self.cars) - 1):
            i = len(self.cars) - h  # i gaat dus van len(self.cars) naar (en inclusief) 2
            for j in xrange(0, i):
                if self.cars[j].collide_distance < self.cars[j + 1].collide_distance or self.cars[j + 1].finished:
                    temp = self.cars[j]
                    self.cars[j] = self.cars[j + 1]
                    self.cars[j + 1] = temp

        # Draw a circle around the best car
        Circle(Point(self.cars[0].x, self.cars[0].y), 10).draw(self.road.win)

        # Create array with only the fitnesses of the cars
        fitnesses = []
        for car in self.cars:
            fitnesses.append(car.collide_distance)

        print "Generation   :", self.generation
        # Max fitness:
        if fitnesses[0] > self.max_fitness:
            self.max_fitness = self.cars[0].collide_distance
        print "Max fitness  :", self.max_fitness
        # Average fitness:
        self.avg_fitness = sum(fitnesses) / len(fitnesses)
        print "Avg fitness  :", self.avg_fitness
        # Best car:
        print "Best car id  :", self.cars[0].id

        # Count finished cars
        finished = 0
        for car in self.cars:
            if car.finished:
                finished += 1
        print "Cars finished: %i/%i (%.1f%%)" % (finished, len(self.cars), 1. * finished / len(self.cars) * 100)
        if finished >= .5 * len(self.cars):
            print "Goal achieved in", self.generation, "generations"
            return True

        print

        time.sleep(.2)
        return False
