import road
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
    finish = []
    back_check = []
    editing_now = inner_points

    print "Start drawing the inner points. Click the button when you're done."

    while 1 + 1 == 2:
        mouse = win.getMouse()

        if button_left <= mouse.x <= button_right and button_top <= mouse.y <= button_right:
            # Button is clicked

            if len(editing_now) < 3 and editing_now is not finish and editing_now is not back_check:
                print "Please draw something"
                continue

            # noinspection PyUnboundLocalVariable
            Line(first_point, editing_now[0]).draw(win)

            # Switch editing_now to new point array
            if editing_now is inner_points:
                editing_now = outer_points
                print "Now draw the outer points."
            elif editing_now is outer_points:
                editing_now = distance_check
                print "And now the distance check."
            elif editing_now is distance_check:
                editing_now = finish
                print "Now put a dot for the starting point and finish"
            elif editing_now is finish:
                editing_now = back_check
                print "Now draw the back check"
            elif editing_now is back_check:
                print "You are done!"
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
    for array in [inner_points, outer_points, distance_check, finish, back_check]:
        for i in range(0, len(array)):
            string += str(array[i].x) + "," + str(array[i].y)

            if i == len(array) - 1:
                string += "\n"
            else:
                string += ",,"

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

    return file_name


def parse_road(name):
    file1 = open("roads/" + name + ".road")
    string1 = file1.read()
    file1.close()

    arrays = string1.splitlines()

    inner_points = []
    outer_points = []
    distance_check = []
    finish = []
    back_check = []
    all_arrays = [inner_points, outer_points, distance_check, finish, back_check]

    for i in range(0, len(arrays)):
        pts = arrays[i].split(",,")
        for pt in pts:
            xy = pt.split(",")
            all_arrays[i].append(Point(int(xy[0]), int(xy[1])))

    return Road(inner_points, outer_points, distance_check, finish, back_check)


def fetch_road():
    name = raw_input("What road? Type \"new\" to creat a new one.\n")
    if name == "new":
        name = make_road()
    return parse_road(name)
