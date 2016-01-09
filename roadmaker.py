from graphics import *
from road import *


def make_road():
    # Make window
    win = GraphWin(title="Road maker", width=road.window_width, height=road.window_height)
    win.setBackground(color_rgb(255, 255, 255))

    # Make button
    button_left = 540
    button_top = 385
    button_right = 595
    button_bottom = 395
    button = Rectangle(Point(button_left, button_top), Point(button_right, button_bottom))
    button.draw(win)

    # Make point arrays
    inner_points = []
    outer_points = []
    distance_check = []
    editing_now = inner_points

    print "Start drawing the inner points. Click the button when you're done."

    while 1 + 1 == 2:
        mouse = win.getMouse()

        if not (
            not (button_left <= mouse.x <= button_right) or not (mouse.y >= button_top)) and mouse.y <= button_bottom:
            # Button is clicked

            if len(editing_now) < 3:
                print "Please draw something"
                continue

            # noinspection PyUnboundLocalVariable
            Line(first_point, editing_now[0]).draw(win)

            # Switch editing_now to new point array
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


def parse_road(name):
    file1 = open("roads/" + name + ".road")
    string1 = file1.read()
    file1.close()

    arrays = string1.splitlines()

    inner_points = []
    outer_points = []
    distance_check = []
    all_arrays = [inner_points, outer_points, distance_check]

    for i in range(0, len(arrays)):
        pts = arrays[i].split(",,")
        for pt in pts:
            xy = pt.split(",")
            all_arrays[i].append(Point(int(xy[0]), int(xy[1])))

    road = Road()
    # TODO road.setRoad(inner_points, outer_points, distance_check)
    return road
