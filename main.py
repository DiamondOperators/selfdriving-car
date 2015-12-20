from ANN import *
from selector import *

ann = ANN()


def func():
    selector = Selector()
    selector.initial_generation()
    selector.test_generation()
    selector.create_next_generation()

    input("Press return to exit")
