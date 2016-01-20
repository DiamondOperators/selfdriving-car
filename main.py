from ANN import ANN
from selector import Selector
from backpropagator import Backpropagator
import roadmaker

ann = ANN()
road = None


def func():
    road = roadmaker.fetch_road()
    option = input("1) Neuroevolution\n2) Backpropagation\n")
    if option == 1:
        selector = Selector()
        selector.initial_generation()
        selector.test_generation()

        while 1 + 1 == 2:
            selector.road.reset_win()
            selector.create_next_generation()
            selector.test_generation()
    elif option == 2:
        pass
    else:
        print "Please choose 1 or 2 or press Ctrl-C"
        func()


if __name__ == "__main__":
    func()
