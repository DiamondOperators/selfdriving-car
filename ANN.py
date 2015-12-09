import tensorflow as tf
import random


class ANN:
    def __init__(self):
        self.inputNodes = 7
        self.hiddenNodes = 64
        self.outputNodes = 1

        self.x = tf.placeholder("float", shape=[self.inputNodes, None], name="sensor-input")
        self.W1 = tf.Variable(tf.random_normal([self.inputNodes, self.hiddenNodes]), name="W1")
        self.W2 = tf.Variable(tf.random_normal([self.hiddenNodes, self.outputNodes]), name="W2")
        self.y = tf.matmul(tf.matmul(self.x, self.W1), self.W2)

        self.session = tf.Session()
        init = tf.initialize_all_variables()
        self.session.run(init)

    def inherit_from(self, parents):
        w1 = []
        for i in range(self.inputNodes):
            w1i = []
            for j in range(self.hiddenNodes):
                parent = parents[random.randint(0, len(parents))]
                parent_w1 = self.session.run(parent.W1)
                w1i.append(parent_w1[i][j])
            w1.append(w1i)
        self.W1 = tf.Variable(w1)

        w2 = []
        for i in range(self.hiddenNodes):
            w2i = []
            for j in range(self.outputNodes):
                parent = parents[random.randint(0, len(parents))]
                parent_w2 = self.session.run(parent.W2)
                w2i.append(parent_w2[i][j])
            w2.append(w2i)
        self.W2 = tf.Variable(w2)

    def propagate_forward(self, sensor_data):
        return self.session.run(self.y, feed_dict={self.x: sensor_data})[0]
