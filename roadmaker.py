from graphics import *

# Make window
win = GraphWin(title="Road maker", width=600, height=400)
win.setBackground(color_rgb(255, 255, 255))

# Make button
buttonLeft = 540
buttonTop = 385
buttonRight = 595
buttonBottom = 395
button = Rectangle(Point(buttonLeft, buttonTop), Point(buttonRight, buttonBottom))
button.draw(win)

# Make point arrays
inner_points = []
outer_points = []
distance_check = []
editing_now = inner_points

while 1 + 1 == 2:
    mouse = win.getMouse()

    if not (not (buttonLeft <= mouse.x <= buttonRight) or not (mouse.y >= buttonTop)) and mouse.y <= buttonBottom:
        print "Button clicked"
        # Button was clicked, switch editing_now to new point array
        if editing_now == inner_points:
            editing_now = outer_points
        elif editing_now == outer_points:
            editing_now = distance_check
        elif editing_now == distance_check:
            break
        continue

    if len(editing_now) == 0:
        # Point(mouse.x, mouse.y).draw(win)
        first_point = Point(mouse.x, mouse.y)
        first_point.draw(win)
        print "First point drawn"
    else:
        last_point = Point(mouse.x, mouse.y)
        last_point.draw(win)
        line = Line(last_point, first_point)
        line.draw(win)
        first_point = last_point
        print "Line drawn"
    editing_now.append(mouse)

# Construct file
string = ""
for i in range(0, len(inner_points)):
    pt = inner_points[i]
    string += pt.x + "," + pt.y

    if i == len(inner_points) - 1:
        string += "\n"
    else:
        string += ",,"
for i in range(0, len(outer_points)):
    pt = outer_points[i]
    string += pt.x + "," + pt.y

    if i == len(outer_points) - 1:
        string += "\n"
    else:
        string += ",,"
for i in range(0, len(distance_check)):
    pt = distance_check[i]
    string += pt.x + "," + pt.y

    if i == len(distance_check) - 1:
        string += "\n"
    else:
        string += ",,"
print string

# Save file
file_name = raw_input("How do you want to call your road? ")
road_file = open("roads/" + file_name, 'w')
road_file.write(string)
road_file.close()
print "File saved successfully"