import tensorflow as tf
import random


class ANN:
    def __init__(self):
        self.inputNodes = 7
        self.hiddenNodes = 64
        self.outputNodes = 1

        self.x = tf.placeholder("float", shape=[self.inputNodes, None], name="sensor-input")
        self.W1 = tf.placeholder("float", shape=[self.inputNodes, self.hiddenNodes])
        self.W2 = tf.placeholder("float", shape=[self.hiddenNodes, self.outputNodes])
        self.y = tf.matmul(tf.matmul(self.x, self.W1), self.W2)

        self.W1Array = []
        self.W2Array = []

        self.session = tf.Session()
        init = tf.initialize_all_variables()
        self.session.run(init)

    def inherit_from(self, parents):
        self.W1Array = []
        for i in range(self.inputNodes):
            w1i = []
            for j in range(self.hiddenNodes):
                parent = parents[random.randint(0, len(parents))]
                parent_w1 = self.session.run(parent.W1)
                w1i.append(parent_w1[i][j])
            self.W1Array.append(w1i)

        self.W2Array = []
        for i in range(self.hiddenNodes):
            w2i = []
            for j in range(self.outputNodes):
                parent = parents[random.randint(0, len(parents))]
                parent_w2 = self.session.run(parent.W2)
                w2i.append(parent_w2[i][j])
            self.W2Array.append(w2i)

    def propagate_forward(self, sensor_data):
        return self.session.run(self.y, feed_dict={self.x: sensor_data, self.W1: self.W1Array, self.W2: self.W2Array})[0]
