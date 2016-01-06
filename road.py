import math
import main
from graphics import *


class Road(object):
    def __init__(self):
        self.win = GraphWin(title="Self-driving car", width=600, height=400)
        self.rw = 50  # Road width
        self.road = []
        self.lines = []
        self.cars = []
        self.finish = None
        self.margin = 2
        self.distance_check = []
        self.check_line = None

    def set_road(self, points, finish, check_line):
        self.road = points
        self.make_lines()
        self.finish = finish
        self.check_line = check_line

    def make_lines(self):
        self.lines = []
        self.distance_check = []

        # Inner lines
        for i in range(0, len(self.road)):
            if i == len(self.road) - 1:
                self.lines.append(Line(self.road[i], self.road[0]))
            else:
                self.lines.append(Line(self.road[i], self.road[i + 1]))

        # Copy to distance_check
        for i in self.lines:
            self.distance_check.append(i)

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
            try:
                line.draw(self.win)
                if abs(line.p1.x - line.p2.x) < 20:
                    print line.p1.x, line.p2.x
            except GraphicsError:
                pass

        try:
            self.finish.draw(self.win)
        except GraphicsError:
            pass

        try:
            self.check_line.draw(self.win)
        except GraphicsError:
            pass

        for car in self.cars:
            Point(car.x, car.y).draw(self.win)
            # TODO undraw

    def reset_win(self):
        self.win.close()
        self.win = GraphWin(title="Self-driving car", width=600, height=400)
        # Also clear self.cars array, to start with a clean window
        self.cars = []
        self.redraw()

    def test(self, cars):
        self.cars = cars

        # Set all cars' positions to the finishing/starting line
        self.reset_car_positions()

        step_time = 1

        while self.not_all_cars_collided():
            for car in self.cars:
                if car.collide_distance != -1:
                    continue
                car.update_direction(self.get_sensor_data(car))

                x_diff = math.cos(car.direction) * step_time * car.speed
                y_diff = math.sin(car.direction) * step_time * car.speed
                car.add_position(x_diff, y_diff)

                if self.car_collided(car):
                    car.collide_distance = self.collide_distance(car)

                if distance_to_line_without_range(self.check_line, car.x, car.y) < self.margin:
                    car.checked = True
            self.redraw()
        print "All cars collided"
        return self.cars

    def collide_distance(self, car):
        if not car.checked:
            return 0

        distances = []
        for line in self.distance_check:
            distances.append(distance_to_line_without_range(line, car.x, car.y))

        index = distances.index(min(distances))

        total_distance = 0

        for line in self.distance_check[:index]:
            total_distance += length_of_line(line)

        total_distance += length_of_line(Line(self.distance_check[index].p1, Point(car.x, car.y)))
        return total_distance

    def reset_car_positions(self):
        for car in self.cars:
            car.set_position(self.finish.x, self.finish.y)

    def not_all_cars_collided(self):
        for car in self.cars:
            if car.collide_distance == -1:
                return True
        return False

    def car_collided(self, car):
        for line in self.lines:
            distance = distance_to_line(line, car.x, car.y)
            if distance < self.margin and distance != -1:
                return True
        return False

    def get_sensor_data(self, car):
        result = []

        # Hier is de maximale kijkhoek van de auto 120 graden oftewel 2/3*pi radialen
        view_angle = 2 / 3 * math.pi
        num_of_sensors = main.ann.inputNodes
        angle_per_sensor = view_angle / num_of_sensors
        first_sensor_angle = car.direction - view_angle / 2
        max_sensor_range = car.sensor_range

        for i in range(0, num_of_sensors):
            # De dichtbijste muur tot nu toe
            closest_line = max_sensor_range

            for line in self.lines:
                sensor_angle = first_sensor_angle + i * angle_per_sensor

                # De richtingscoefficient van de sensorlijn
                m1 = math.tan(sensor_angle)

                # Het snijpunt van de sensorlijn met de y-as (als y = mx + b, dan b = y - mx
                b1 = car.y - m1 * car.x

                # De richtingscoefficient van de lijn
                m2 = (line.p2.y - line.p1.y) / (line.p2.x - line.p1.x)

                # Het snijpunt van de lijn met de y-as
                b2 = line.p1.y - m2 * line.p1.x

                if m1 - m2 == 0:
                    # De lijnen lopen parallel
                    continue

                # De coordinaten van het snijpunt van de lijnen
                x = (b2 - b1) / (m1 - m2)
                y = m1 * x + b1

                # De afstand snijpunt tot auto
                d = math.sqrt((x - car.x) ** 2 + (y - car.y) ** 2)

                if d > closest_line:
                    # Geen kandidaat voor dichtsbijzijnde lijn
                    continue

                if not in_range(line, x, y):
                    # Sensorlijn sneedt muurlijn wel, maar niet het muurlijn*segment* dat de echte muur vormt
                    continue

                if math.cos(sensor_angle) * (x - car.x) <= 0:
                    # Het snijpunt van sensorlijn en muurlijn zit aan de verkeerde kant van de auto
                    # (kruist niet met eigenlijke sensorlijnsegment)
                    continue

                # Als deze code wordt bereikt is er alles goed en is het de kortste afstand tot nu toe.
                closest_line = d
            result.append(closest_line)
        return [result]


def in_range(line, x, y):
    return x < min(line.p1.x, line.p2.x) \
           or x > max(line.p1.x, line.p2.x)


def distance_to_line(line, x, y):
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

    s = line.p1
    t = line.p2

    # Eerst kijken of de auto binnen het bereik van de lijn is:
    if in_range(line, x, y):
        return 1000000000000000000

    # Afstand uitrekenen
    a = s.y - t.y
    b = t.x - s.x
    c = s.x * t.y - t.x * s.y
    return abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)


def distance_to_line_without_range(line, x, y):
    s = line.p1
    t = line.p2
    a = s.y - t.y
    b = t.x - s.x
    c = s.x * t.y - t.x * s.y
    return abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)


def length_of_line(line):
    return math.sqrt((line.p1.x - line.p2.x) ** 2 + (line.p1.y - line.p2.y) ** 2)


def test():
    # Test
    road = Road()
    pts = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
           Point(300, 340), Point(150, 320), Point(50, 250)]  # pts = [Point(100, 100), Point(160, 60)]
    road.set_road(pts, Point(300, 35))
    road.redraw()

    input("Press any key to exit")
