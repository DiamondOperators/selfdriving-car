import tensorflow as tf


class ANN:
    def __init__(self):
        self.inputNodes = 7
        self.hiddenNodes = 64
        self.outputNodes = 1

        self.x = tf.placeholder("float", shape=[None, self.inputNodes], name="sensor-input")
        self.W1 = tf.placeholder("float", shape=[self.inputNodes, self.hiddenNodes])
        self.W2 = tf.placeholder("float", shape=[self.hiddenNodes, self.outputNodes])
        self.y = tf.tanh(tf.matmul(tf.tanh(tf.matmul(self.x, self.W1)), self.W2))

        self.session = tf.Session()
        init = tf.initialize_all_variables()
        self.session.run(init)

    def propagate_forward(self, car, sensor_data):
        return self.session.run(self.y, feed_dict={self.x: sensor_data, self.W1: car.W1, self.W2: car.W2})
