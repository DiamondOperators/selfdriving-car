# Car used for backpropagation
# It has its own neural network and tensorflow session

import tensorflow as tf
import main

stddev = .05  # Standard deviation for random weights


class BackpropCar:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.sensor_range = 200
        self.checked = True  # Not necessary for this car, but road.collide_distance() wants it

        self.input = tf.placeholder("float", shape=[None, main.ann.inputNodes], name="sensor-input")
        self.W1 = tf.Variable(tf.random_normal([main.ann.inputNodes, main.ann.hiddenNodes], stddev=stddev))
        self.W2 = tf.Variable(tf.random_normal([main.ann.hiddenNodes, main.ann.hiddenNodes2], stddev=stddev))  # weight3
        self.W3 = tf.Variable(tf.random_normal([main.ann.hiddenNodes2, main.ann.outputNodes], stddev=stddev))  # weight3
        self.output = tf.tanh(
            tf.matmul(tf.tanh(tf.matmul(tf.tanh(tf.matmul(self.input, self.W1)), self.W2)), self.W3))  # weight3

        self.y_ = tf.placeholder("float", shape=[None, 1], name="proper_output")
        self.cost = tf.reduce_mean(tf.square(self.output - self.y_))  # Is this a good cost function?
        self.trainer = tf.train.GradientDescentOptimizer(0.0001).minimize(self.cost)

        self.session = tf.Session()
        self.session.run(tf.initialize_all_variables())

    def update_direction(self, sensor_input):
        self.direction += self.session.run(self.output, feed_dict={self.input: sensor_input})[0][0]

    def train(self, x, y_):
        print "Training..."
        cost_before = self.session.run(self.cost, feed_dict={self.input: x, self.y_: y_})

        for i in xrange(1):
            self.session.run(self.trainer, feed_dict={self.input: x, self.y_: y_})

        cost_after = self.session.run(self.cost, feed_dict={self.input: x, self.y_: y_})
        print "Cost change:", cost_before, "\t-", cost_after, "\t=", (cost_before - cost_after), "\n"
