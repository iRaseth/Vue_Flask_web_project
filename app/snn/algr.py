import numpy as np

class SimpleNeuron():
    def __init__(self, input_data):
        np.random.seed(1)
        self.weights = np.random.random([2])
        self.input = np.array([input_data[0],input_data[1]])
        self.learning_parameter = input_data[3]
        self.d_output = input_data[4]

    def __repr__(self):
        return '<Neuron with weights :{},  and input: {}, returned output : {}>'.format(self.weights, self.input, self.y)
        #return f"Neuron with weights :{self.weights},  and input: {self.input}, returned output : {self.y}"

    def process(self):
        self.u = np.dot(self.input, self.weights)
        if self.d_output == self.u:
            return
        else:
            self.subtract = np.subtract(self.d_output, self.u)
            self.multiplication = self.learning_parameter * self.subtract * self.input
            self.weights = self.weights + self.multiplication

    def train(self, count):
        for _ in range(count):
            self.process()

#neuron = SimpleNeuron(1,0.1,output=2.85)
#print neuron.weights
#for x in range(100):
#    neuron.process()
#print neuron.weights
#print neuron.u
