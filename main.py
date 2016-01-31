from ANN import *
from selector import *
from backpropagator import *

ann = ANN()


def func():
    option = input("1) Neuroevolution\n2) Backpropagation\n")
    if option == 1:
        selector = Selector()
        selector.start()
    elif option == 2:
        Backpropagator()
    else:
        print "Please choose 1 or 2 or press Ctrl-C"
        func()


if __name__ == "__main__":
    func()
