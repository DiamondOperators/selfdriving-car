# Selfdriving car
A neuroevolutionary self driving (software) car.


## Components
###### Car
  - Direction
  - Speed (constant?)
  - Sensors
  - Connected to an ANN
  - Every step that it makes while driving flows trough the ANN

###### Road
  - Show cars
  - Detect collisions
  - Indicate distance traveled by each car

###### Artificial Neural Network
  - Nodes and weights.
  - Variable weights
  - Input: data from car sensors
  - Output: value between -1 (60 degrees to the left) and 1 (60 degrees to the right)

###### Evolver
  - Gets the ANN, tests and reproduces them:
    - Makes 50 cars with random weights
    - Applies the ANN to the cars and measure their distance
    - Selects the 25 best cars
    - Makes 25 new cars with weights inherited from the top 25
    - Applies a mutation
    - Replaces bad 25 with good 25
    - Repeat
