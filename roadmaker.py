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

print "Start drawing the inner points. Click the button when you're done."

while 1 + 1 == 2:
    mouse = win.getMouse()

    if not (not (buttonLeft <= mouse.x <= buttonRight) or not (mouse.y >= buttonTop)) and mouse.y <= buttonBottom:
        Line(first_point, editing_now[0]).draw(win)
        # Button was clicked, switch editing_now to new point array
        if editing_now == inner_points:
            editing_now = outer_points
            print "Now draw the outer points..."
        elif editing_now == outer_points:
            editing_now = distance_check
            print "... and now the distance check."
        elif editing_now == distance_check:
            "You are done!"
            break
        continue

    mouse.draw(win)
    if len(editing_now) == 0:
        first_point = mouse
    else:
        line = Line(mouse, first_point)
        line.draw(win)
        first_point = mouse
    editing_now.append(mouse)

# Construct file
string = ""
for array in [inner_points, outer_points, distance_check]:
    for i in range(0, len(array)):
        string += str(array[i].x) + "," + str(array[i].y)

        if i == len(array) - 1:
            string += "\n"
        else:
            string += ",,"
print "String to be saved:", string

# Save file
try:
    os.mkdir("./roads/")
except OSError:
    # Folder was already created"
    pass

file_name = raw_input("How do you want to call your road? ")
road_file = open("roads/" + file_name + ".road", 'w')
road_file.write(string)
road_file.close()
print "File saved successfully"
