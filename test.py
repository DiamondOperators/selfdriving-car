from graphics import *

class CarWindow(object):

    def __init__(self):
        self.win = GraphWin(title="Self-driving car", width=600, height=450)
        self.setRoad([], [])

    def setRoad(self, innerPoints, outerPoints):
        self.ipt = innerPoints
        self.opt = outerPoints
        self.makeLines()

    def makeLines(self):
        self.lines = []
        for i in range(0, len(self.ipt)):
            if (i == len(self.ipt) - 1):
                self.lines.append(Line(self.ipt[i], self.ipt[0]))
            else:
                self.lines.append(Line(self.ipt[i], self.ipt[i + 1]))

        for i in range(0, len(self.opt)):
            if (i == len(self.opt) - 1):
                self.lines.append(Line(self.opt[i], self.opt[0]))
            else:
                self.lines.append(Line(self.opt[i], self.opt[i + 1]))

    def redraw(self):
        for line in self.lines:
            line.draw(self.win)


# Test
win = CarWindow()
ipts = [Point(300, 50), Point(400, 60), Point(475, 80), Point(400, 200)]
opts = [Point(300, 20), Point(420, 60), Point(495, 80), Point(400, 250)]
win.setRoad(ipts, opts)
win.redraw()
