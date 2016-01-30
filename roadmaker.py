import road
from road import *


def make_road():
    # Make window
    win = GraphWin(title="Road maker", width=road.window_width, height=road.window_height)
    win.setBackground(color_rgb(255, 255, 255))

    button_width = 50
    button_height = 10
    button_margin = 5

    # 'Done' button
    button_left = road.window_width - button_margin - button_width
    button_top = road.window_height - button_margin - button_height
    button_right = road.window_width - button_margin
    button_bottom = road.window_height - button_margin
    button = Rectangle(Point(button_left, button_top), Point(button_right, button_bottom))
    button.draw(win)

    # Maak de weg rond
    button_left2 = road.window_width - 2 * button_margin - 2 * button_width
    button_top2 = road.window_height - button_margin - button_height
    button_right2 = road.window_width - 2 * button_margin - button_width
    button_bottom2 = road.window_height - button_margin
    button2 = Rectangle(Point(button_left2, button_top2), Point(button_right2, button_bottom2))
    button2.draw(win)

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

        if button_left2 <= mouse.x <= button_right2 and button_top2 <= mouse.y <= button_right2:
            # Left button was clicked
            if len(editing_now) < 3 or editing_now is finish or editing_now is back_check:
                print "You cannot perform that operation"
                continue
            mouse = Point(editing_now[0].x, editing_now[0].y)

        elif button_left <= mouse.x <= button_right and button_top <= mouse.y <= button_right:
            # Right button was clicked
            if len(editing_now) < 3 and editing_now is not finish and editing_now is not back_check:
                print "Please draw something"
                continue

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

    print "Starting direction"
    mouse = win.getMouse()
    starting_direction = math.atan2(float(mouse.y) - float(finish[0].y), float(mouse.x) - float(finish[0].x))
    print "Calculated direction:", starting_direction, "radians"

    # Construct file
    string = ""
    for array in [inner_points, outer_points, distance_check, finish, back_check]:
        for i in range(0, len(array)):
            string += str(array[i].x) + "," + str(array[i].y)

            if i == len(array) - 1:
                string += "\n"
            else:
                string += ",,"
    string += str(starting_direction) + "\n"

    # Save file
    try:
        os.mkdir("./roads/")
    except OSError:
        # Folder was already created"
        pass

    file_name = raw_input("What do you want to call your road? ")
    road_file = open("roads/" + file_name + ".road", 'w')
    road_file.write(string)
    road_file.close()
    print "File saved successfully"

    return file_name


def parse_road(name):
    file1 = open("roads/" + name + ".road")
    string1 = file1.read()
    file1.close()

    lines = string1.splitlines()

    inner_points = []
    outer_points = []
    distance_check = []
    finish = []
    back_check = []
    all_arrays = [inner_points, outer_points, distance_check, finish, back_check]

    for i in range(0, len(all_arrays)):
        pts = lines[i].split(",,")
        for pt in pts:
            xy = pt.split(",")
            all_arrays[i].append(Point(int(xy[0]), int(xy[1])))
    starting_direction = float(lines[5])

    return road.Road(inner_points, outer_points, distance_check, finish, back_check, starting_direction)


def fetch_road():
    name = raw_input("What road? Type \"new\" to create a new one.\n")
    if name == "new":
        name = make_road()
    return parse_road(name)
