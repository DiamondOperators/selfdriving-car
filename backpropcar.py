# Car used for backpropagation
# It has its own neural network and tensorflow session

import tensorflow as tf
import main

stddev = .2  # Standard deviation for random weights


class BackpropCar:
    def __init__(self):
        self.speed = 2
        self.x = 0
        self.y = 0
        self.direction = 0
        self.sensor_range = 200

        self.x = tf.placeholder("float", shape=[None, main.ann.inputNodes], name="sensor-input")
        self.W1 = tf.Variable(tf.random_normal([main.ann.inputNodes, main.ann.hiddenNodes], stddev=stddev))
        self.W2 = tf.Variable(tf.random_normal([main.ann.hiddenNodes, main.ann.hiddenNodes2], stddev=stddev))  # weight3
        self.W3 = tf.Variable(tf.random_normal([main.ann.hiddenNodes2, main.ann.outputNodes], stddev=stddev))  # weight3
        self.y = tf.tanh(
            tf.matmul(tf.tanh(tf.matmul(tf.tanh(tf.matmul(self.x, self.W1)), self.W2)), self.W3))  # weight3

        self.y_ = tf.placeholder("float", shape=[None, 1], name="proper_output")
        self.cost = tf.reduce_mean(tf.square(self.y - self.y_))  # Is this a good cost function?
        self.trainer = tf.train.GradientDescentOptimizer(0.8).minimize(self.cost)

        self.session = tf.Session()
        self.session.run(tf.initialize_all_variables())

    def update_direction(self, sensor_input):
        self.direction += self.session.run(self.y, feed_dict={self.x: sensor_input})

    def train(self, x, y_):
        print "Cost function output before:", self.session.run(self.cost, feed_dict={self.x: x, self.y_: y_})
        for i in xrange(100):
            self.session.run(self.trainer, feed_dict={self.x: x, self.y_: y})
        print "Cost function output after :", self.session.run(self.cost, feed_dict={self.x: x, self.y_: y_})
