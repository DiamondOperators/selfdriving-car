from graphics import *
import math

class CarWindow(object):

    def __init__(self):
        self.win = GraphWin(title="Self-driving car", width=600, height=400)
        self.rw = 20

    def setRoad(self, pts):
        self.road = pts
        self.makeLines()

    def makeLines(self):
        self.lines = []

        # Inner lines
        for i in range(0, len(self.road)):
            if (i == len(self.road) - 1):
                self.lines.append(Line(self.road[i], self.road[0]))
            else:
                self.lines.append(Line(self.road[i], self.road[i + 1]))

        # Outer points
        outerPoints = []
        for i in range(0, len(self.road)):
            pt1 = self.road[i]
            if (i == len(self.road) - 1):
                pt2 = self.road[0]
            else:
                pt2 = self.road[i + 1]

            x_diff = float(pt2.x - pt1.x)
            y_diff = float(pt2.y - pt1.y)
            alpha = math.atan(y_diff / x_diff)

            x = self.rw * math.sin(alpha)
            y = self.rw * math.cos(alpha)

##            if (x_diff > 0):
##                if (y_diff > 0):
##                    outerPoints.append(Point(pt1.x - x, pt1.y - y))
##                    outerPoints.append(Point(pt2.x - x, pt2.y - y))
##                else:
##                    outerPoints.append(Point(pt1.x - x, pt1.y + y))
##                    outerPoints.append(Point(pt2.x - x, pt2.y + y))
##            else:
##                if (y_diff > 0):
##                    outerPoints.append(Point(pt1.x + x, pt1.y - y))
##                    outerPoints.append(Point(pt2.x + x, pt2.y - y))
##                else:
##                    outerPoints.append(Point(pt1.x + x, pt1.y + y))
##                    outerPoints.append(Point(pt2.x + x, pt2.y + y))

            outerPoints.append(Point(pt1.x - x, pt1.y - y))
            outerPoints.append(Point(pt2.x - x, pt2.y - y))

        # Outer lines
        for i in range(0, len(outerPoints)):
            if (i == len(outerPoints) - 1):
                self.lines.append(Line(outerPoints[i], outerPoints[0]))
            else:
                self.lines.append(Line(outerPoints[i], outerPoints[i + 1]))

    def draw(self):
        for line in self.lines:
            line.draw(self.win)


# Test
carWindow = CarWindow()
pts = [Point(100, 100), Point(300, 50), Point(500, 100), Point(400, 300),
       Point(150, 320)]
carWindow.setRoad(pts)
carWindow.draw()
