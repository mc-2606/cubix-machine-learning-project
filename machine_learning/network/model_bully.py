# Importing machine learning modules
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.losses import SparseCategoricalCrossentropy
from matplotlib import pyplot as plt


# File saving
from datetime import datetime
from json import dump, load

# The Model Handler
class Model:


    # Constructor
    def __init__(self, hidden_layer_count=None, layer_sizes=None, output_neuron_count=None, hidden_activation_func=None, output_activation_func=None, loss_function=None, metrics=None, learning_rate=None):
        # Network parameters
        self.hidden_layer_count = hidden_layer_count
        self.layer_sizes = layer_sizes
        self.output_neuron_count = output_neuron_count
        self.hidden_activation_func = hidden_activation_func
        self.output_activation_func = output_activation_func


        # Training variables
        self.loss_function = loss_function
        self.metrics = metrics
        self.learning_rate = learning_rate
        self.optimiser = None


        # The actual model/network
        self.model = Sequential()

    # Constructs the layers into the model
    def build_model(self):
        # Adding the required input layers
        for count in range(self.hidden_layer_count):
            # Creating the new layer
            layer = Dense(units=(self.layer_sizes[count]), activation=self.hidden_activation_func, name=f"layer_{count}")

            # Adding the layer
            self.model.add(layer)

        # Adding the output layer
        output_layer = Dense(units=(self.output_neuron_count), activation=self.output_activation_func, name="layer_output")
        self.model.add(output_layer)


# Creating new model    
model = Model(2, [1, 1], 19, 'relu', 'softmax')
model.build_model()
track_layers = model.model.layers
len(track_layers)

