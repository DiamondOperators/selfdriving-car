import math
import main
from graphics import *

window_width = 600
window_height = 400


class Road(object):
    def __init__(self, inner_points=None, outer_points=None, distance_check_points=None,
                 finish=None, back_check=None, starting_direction=None):
        self.win = GraphWin(title="Self-driving car", width=window_width, height=window_height)
        self.rw = 50  # Road width
        self.road = []
        self.lines = []
        self.cars = []
        self.finish = None
        self.starting_direction = None
        self.margin = 2
        self.back_check = None
        self.distance_check = []

        if inner_points is not None and outer_points is not None \
                and distance_check_points is not None and finish is not None \
                and back_check is not None and starting_direction is not None:
            self.inner_points = inner_points
            self.outer_points = outer_points
            self.distance_check_points = distance_check_points
            self.make_lines()
            self.finish = finish[0]
            self.back_check = Line(back_check[0], back_check[1])
            self.starting_direction = starting_direction

    def make_lines(self):
        # Clear lists
        self.lines = []
        self.distance_check = []

        # Road lines
        for point_array in [self.inner_points, self.outer_points]:
            for i in range(0, len(point_array) - 1):
                self.lines.append(Line(point_array[i], point_array[i + 1]))
        # Distance check lines
        for i in range(0, len(self.distance_check_points) - 1):
            self.distance_check.append(Line(self.distance_check_points[i], self.distance_check_points[i + 1]))

    def redraw(self):
        for line in self.lines + self.distance_check:
            try:
                line.draw(self.win)
            except GraphicsError:
                pass

        try:
            self.finish.draw(self.win)
        except GraphicsError:
            pass

        try:
            self.back_check.draw(self.win)
        except GraphicsError:
            pass

        for car in self.cars:
            Point(car.x, car.y).draw(self.win)

    def reset_win(self):
        self.win.close()
        self.win = GraphWin(title="Self-driving car", width=window_width, height=window_height)
        # Also clear self.cars array, to start with a clean window
        self.cars = []
        self.redraw()

    def test(self, cars):
        self.cars = cars

        self.reset_cars()

        step_time = 1

        while self.not_all_cars_collided():
            for car in cars:
                if car.collide_distance != -1:
                    continue
                car.update_direction(self.get_sensor_data(car))

                x_diff = math.cos(car.direction) * step_time * car.speed
                y_diff = math.sin(car.direction) * step_time * car.speed
                car.add_position(x_diff, y_diff)

                if self.car_collided(car):
                    car.collide_distance = self.collide_distance(car)

                if self.point_collides_with_line(self.back_check, car.x, car.y):
                    car.checked = True
            self.redraw()

    def collide_distance(self, car):
        if not car.checked:
            return 0

        distances = []
        for line in self.distance_check:
            distances.append(distance_to_line_segment(line, car))

        index = distances.index(min(distances))

        total_distance = 0

        for line in self.distance_check[:index]:
            total_distance += length_of_line(line)

        current_segment = self.distance_check[index]
        total_distance += math.sqrt((car.x - current_segment.p1.x) ** 2 + (car.y - current_segment.p1.y) ** 2)
        return total_distance

    def reset_cars(self):
        for car in self.cars:
            car.checked = False
            car.set_position(self.finish.x, self.finish.y)
            car.collide_distance = -1
            car.direction = self.starting_direction

    def not_all_cars_collided(self):
        for car in self.cars:
            if car.collide_distance == -1:
                return True
        return False

    def car_collided(self, car):
        for line in self.lines:
            if self.point_collides_with_line(line, car.x, car.y):
                return True
        return False

    def get_sensor_data(self, car):
        result = []

        # Hier is de maximale kijkhoek van de auto 120 graden oftewel 2/3*pi radialen
        view_angle = 2. / 3 * math.pi
        num_of_sensors = main.ann.inputNodes
        angle_per_sensor = view_angle / (num_of_sensors - 1)
        first_sensor_angle = car.direction - view_angle / 2
        max_sensor_range = car.sensor_range

        for i in range(0, num_of_sensors):
            sensor_angle = first_sensor_angle + i * angle_per_sensor

            # De dichtbijste muur tot nu toe voor deze sensor
            closest_line = max_sensor_range

            for wall in self.lines:
                # De richtingscoefficient van de sensorlijn
                m1 = math.tan(sensor_angle)

                # Het snijpunt van de sensorlijn met de y-as (als y = mx + b, dan b = y - mx)
                b1 = car.y - m1 * car.x

                if wall.p2.x == wall.p1.x:
                    # De muurlijn is verticaal. We moeten de coordinaten van het snijpunt
                    # nu anders berekenen, anders moeten we delen door nul
                    # Neem de x van de verticale muurlijn:
                    x = wall.p1.x
                    # En bereken de y door de x in te vullen in de sensorlijn formule:
                    y = m1 * x + b1
                else:
                    # De richtingscoefficient van de muurlijn:
                    m2 = (wall.p2.y - wall.p1.y) / (wall.p2.x - wall.p1.x)

                    # Het snijpunt van de muurlijn met de y-as:
                    b2 = wall.p1.y - m2 * wall.p1.x

                    if m1 - m2 == 0:
                        # De lijnen lopen parallel dus er is geen snijpunt
                        continue

                    # De coordinaten van het snijpunt van de lijnen
                    x = (b2 - b1) / (m1 - m2)
                    y = m1 * x + b1

                # De afstand snijpunt tot auto
                d = math.sqrt((x - car.x) ** 2 + (y - car.y) ** 2)

                if d > closest_line:
                    # Geen kandidaat voor dichtsbijzijnde lijn
                    continue

                if out_of_range(wall, x, y):
                    # Sensorlijn snijdt muurlijn wel, maar niet het muurlijn*segment* dat de echte muur vormt
                    continue

                if math.cos(sensor_angle) * (x - car.x) <= 0:
                    # Het snijpunt van sensorlijn en muurlijn zit aan de verkeerde kant van de auto
                    # (kruist niet met eigenlijke sensorlijnsegment)
                    continue

                # Als deze code wordt bereikt is alles goed en is het de kortste afstand tot nu toe.
                closest_line = d
            result.append(closest_line)
        return [result]

    def point_collides_with_line(self, line, x, y):
        # Eerst kijken of de auto binnen het bereik van de lijn is:
        if out_of_range(line, x, y):
            return False

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

        # Afstand berekenen
        a = s.y - t.y
        b = t.x - s.x
        c = s.x * t.y - t.x * s.y
        distance = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
        return distance < self.margin


def out_of_range(line, x, y):
    minx = min(line.p1.x, line.p2.x)
    maxx = max(line.p1.x, line.p2.x)
    miny = min(line.p1.y, line.p2.y)
    maxy = max(line.p1.y, line.p2.y)
    return (x < minx or x > maxx) and (y < miny or y > maxy)


def distance_to_line_segment(line, car):
    s = line.p1
    t = line.p2

    if t.x - s.x == 0:
        # De lijn is verticaal
        if min(s.y, t.y) <= car.y <= max(s.y, t.y):
            return abs(car.x - t.x)
        else:
            return closest_end_point(line, car.x, car.y)
    if t.y - s.y == 0:
        # De lijn is horizontaal
        if min(s.x, t.x) <= car.x <= max(s.x, t.x):
            return abs(car.y - t.y)
        else:
            return closest_end_point(line, car.x, car.y)

    # Richtingscoefficient van de lijn:
    m1 = (t.y - s.y) * 1. / (t.x - s.x)
    b1 = s.y - m1 * s.x

    # Richtingscoefficient van de lijn uit het punt (car.x, car.y) die loodrecht op het lijnsegment staat:
    m2 = -1. / m1
    b2 = car.y - m2 * car.x

    # Snijpunt van de lijnen:
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    if out_of_range(line, x, y):
        return closest_end_point(line, car.x, car.y)
    else:
        # Wiskunde D formule
        a = s.y - t.y
        b = t.x - s.x
        c = s.x * t.y - t.x * s.y
        return abs(a * car.x + b * car.y + c) / math.sqrt(a ** 2 + b ** 2)


def closest_end_point(line, x, y):
    # Find the closest of the two end points of the line
    d1 = math.sqrt((x - line.p1.x) ** 2 + (y - line.p1.y) ** 2)
    d2 = math.sqrt((x - line.p2.x) ** 2 + (y - line.p2.y) ** 2)
    return min(d1, d2)


def length_of_line(line):
    return math.sqrt((line.p1.x - line.p2.x) ** 2 + (line.p1.y - line.p2.y) ** 2)

# import roadmaker
# from car import *
# from ANN import *
#
#
# def test():
#     # Test
#     main.ann = ANN()
#     road = roadmaker.fetch_road()
#     distance_check_pts = [Point(100, 100), Point(200, 100), Point(200, 200), Point(100, 200)]
#     distance_check_lines = []
#     for i in range(0, len(distance_check_pts)):
#         if i == len(distance_check_pts) - 1:
#             distance_check_lines.append(Line(distance_check_pts[i], distance_check_pts[0]))
#         else:
#             distance_check_lines.append(Line(distance_check_pts[i], distance_check_pts[i + 1]))
#     road.distance_check = distance_check_lines
#     road.redraw()
#     for i in road.distance_check:
#         i.draw(road.win)
#     car = Car()
#     while True:
#         mouse = road.win.getMouse()
#         car.x = mouse.x
#         car.y = mouse.y
#         road.collide_distance(car)
