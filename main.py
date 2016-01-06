from ANN import *
from selector import *

ann = ANN()


def func():
    selector = Selector()
    selector.initial_generation()
    selector.test_generation()

    while 1 + 1 == 2:
        selector.road.reset_win()
        selector.create_next_generation()
        selector.test_generation()

    input("Press return to exit")

if __name__ == "__main__":
    func()
