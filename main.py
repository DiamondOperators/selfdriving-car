from ANN import *
from selector import *

ann = ANN()


def func():
    selector = Selector()
    selector.initial_generation()
    selector.test_generation()

    while 1 + 1 == 2:
        raw_input("Press Enter to test new generation")
        selector.road.reset_win()
        selector.create_next_generation()
        selector.test_generation()

    input("Press return to exit")
