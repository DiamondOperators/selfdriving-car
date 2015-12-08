from graphics import *
import math


class Road(object):
    def __init__(self):
        self.win = GraphWin(title="Self-driving car", width=600, height=400)
        self.rw = 30
        self.road = []
        self.lines = []

    def set_road(self, points):
        self.road = points
        self.make_lines()

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

    def draw(self):
        for line in self.lines:
            line.draw(self.win)


# Test
road = Road()
pts = [Point(100, 100), Point(300, 50), Point(500, 100), Point(501, 200), Point(450, 300),
       Point(300, 340), Point(150, 320), Point(50, 250)]  # pts = [Point(100, 100), Point(160, 60)]
road.set_road(pts)
road.draw()

input("Press any key to exit")
