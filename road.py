import math
from graphics import *


class Road(object):
    def __init__(self):
        self.win = GraphWin(title="Self-driving car", width=600, height=400)
        self.rw = 30  # Road width
        self.road = []
        self.lines = []
        self.cars = []
        self.finish = None
        self.margin = 2

    def set_road(self, points, finish):
        self.road = points
        self.make_lines()
        self.finish = finish

    def make_lines(self):
        self.lines = []

        # Inner lines
        for i in range(0, len(self.road)):
            if i == len(self.road) - 1:
                self.lines.append(Line(self.road[i], self.road[0]))
            else:
                self.lines.append(Line(self.road[i], self.road[i + 1]))

        # Outer points
        outer_points = []
        for i in range(0, len(self.road)):
            pt1 = self.road[i]
            if i == len(self.road) - 1:
                pt2 = self.road[0]
            else:
                pt2 = self.road[i + 1]

            x_diff = float(pt2.x - pt1.x)
            y_diff = float(pt2.y - pt1.y)
            alpha = math.atan(y_diff / x_diff)

            x = self.rw * math.sin(alpha)
            y = self.rw * math.cos(alpha)

            if x_diff < 0:
                outer_points.append(Point(pt1.x - x, pt1.y + y))
                outer_points.append(Point(pt2.x - x, pt2.y + y))
            else:
                outer_points.append(Point(pt1.x + x, pt1.y - y))
                outer_points.append(Point(pt2.x + x, pt2.y - y))

        # Outer lines
        for i in range(0, len(outer_points)):
            if i == len(outer_points) - 1:
                self.lines.append(Line(outer_points[i], outer_points[0]))
            else:
                self.lines.append(Line(outer_points[i], outer_points[i + 1]))

    def redraw(self):
        for line in self.lines:
            line.draw(self.win)
        self.finish.draw(self.win)
        for car in self.cars:
            Point(car.x, car.y).draw(self.win)

    def test(self, cars):
        self.cars = cars

        step_time = 1

        while self.not_all_cars_collided():
            for car in cars:
                if car.collide_distance != -1:
                    break
                car.update_direction(self.get_sensor_data(car))

                x_diff = math.cos(car.direction) * step_time * car.speed
                y_diff = math.sin(car.direction) * step_time * car.speed
                car.add_position(x_diff, y_diff)

                if self.car_collided(car):
                    # TODO car.collide_distance bepalen
                    car.collide_distance = 2  # Random
            self.redraw()
        return cars

    def not_all_cars_collided(self):
        for car in self.cars:
            if car.collide_distance == -1:
                return True
        return False

    def car_collided(self, car):
        # Afstand van punt tot lijn.
        # Lijn:
        #   ax + by + c = 0
        # Punt:
        #   (p, q)
        # Formule voor afstand:
        #   |ap + bq + c| / sqrt(a^2 + b^2)

        # Vergelijking van lijn opstelling aan de hand van twee punten (s en t):
        # (sy - ty)x + (tx - sx)y + (sxty - txsy) = 0
        # Dus:
        #   a = sy - ty
        #   b = tx - sx
        #   c = sx*ty - tx*sy

        for line in self.lines:
            s = line.p1, t = line.p2

            # Eerst kijken of de auto binnen het bereik van de lijn is:
            if car.x < min(s.x, t.x) or car.x > max(s.x, t.x) or car.y < min(s.y, t.y) or car.y > max(s.y, t.y):
                continue

            # Afstand uitrekenen
            a = s.y - t.y
            b = t.x - s.x
            c = s.x * t.y - t.x * s.y
            distance = abs(a * car.x + b * car.y + c) / math.sqrt(a ** 2 + b ** 2)

            if distance < self.margin:
                return True

        return False

    def get_sensor_data(self, car):
        pass


def test():
    # Test
    road = Road()
    pts = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
           Point(300, 340), Point(150, 320), Point(50, 250)]  # pts = [Point(100, 100), Point(160, 60)]
    road.set_road(pts, Point(300, 35))
    road.redraw()

    input("Press any key to exit")
