from ANN import *
from selector import *

ann = ANN()

selector = Selector()
selector.initial_generation()
selector.test_generation()
selector.create_next_generation()
