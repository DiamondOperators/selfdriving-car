import tensorflow as tf
import random


class ANN:
    def __init__(self):
        self.inputNodes = 7
        self.hiddenNodes = 64
        self.outputNodes = 1

        self.x = tf.placeholder("float", shape=[inputNodes, None], name="Sensor input")
        self.W1 = tf.Variable(tf.random_normal([self.inputNodes, self.hiddenNodes]), name="W1")
        self.W2 = tf.Variable(tf.random_normal([self.hiddenNodes, self.outputNodes]), name="W2")
        self.y = tf.matmul(tf.matmul(self.x, self.W1), self.W2)

        self.session = tf.Session()
        init = tf.initialize_all_variables()
        self.session.run(init)

    def inherit_from(self, parents):
        w1 = self.session.run(self.W1)
        for i in w1:
            parent = parents[random.randint(0, len(parents))]
            w1[i] = parent[i]

    def adjust_direction(self, sensor_data):
        return self.session.run(self.y, feed_dict={self.x: sensor_data})[0]
