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

# CONSTANTS
CHECKPOINT_PATH_TF = "network/checkpoint/checkpoint_files/"


# The Model Handler
class Model:

    # Constructor
    def __init__(self, hidden_layer_count=None, layer_sizes=None, output_neuron_count=None, hidden_activation_func=None, output_activation_func=None, metrics=None, learning_rate=None):
        # Network parameters
        self.hidden_layer_count = hidden_layer_count
        self.layer_sizes = layer_sizes
        self.output_neuron_count = output_neuron_count
        self.hidden_activation_func = hidden_activation_func
        self.output_activation_func = output_activation_func

        # Training variables
        self.loss_function = None
        self.metrics = metrics
        self.learning_rate = learning_rate
        self.optimiser = None
        self.checkpoint_callback = None

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
    
    # The SGD (calc)
    def build_optimiser(self):
        self.optimiser = Adam(learning_rate=self.learning_rate)
    
    # Adding loss function
    def compile_model(self):
        # Using sparse cross entropy loss function
        self.loss_function = SparseCategoricalCrossentropy()

        # Compiling the model with optimisers, loss and metrics
        self.model.compile(optimizer=self.optimiser,
                           loss=self.loss_function,
                           metrics="accuracy")

    # Creates a callback checkpoint
    def build_checkpoint(self):
        # Fetching current time and logging variables
        current_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        path_name = f"{CHECKPOINT_PATH_TF}{current_time}.ckpt"


        # Creating the checkpoint callback
        self.checkpoint_callback = ModelCheckpoint(filepath=path_name,
                                     verbose=1, # Set on logging for testing purposes
                                     save_best_only=True,
                                     monitor="accuracy")
    
    # Trainig the model
    def train(self, features_train, features_validate, labels_train, labels_validate, epochs):

        # Passing in training info
        history = self.model.fit(
            x=features_train,
            y=labels_train,
            validation_data=[features_validate, labels_validate],
            callbacks=self.checkpoint_callback,
            epochs=epochs,
        )

        # Printing out accuracy
        print(history.history['accuracy'])


# Creating new model    
model = Model(2, [1, 1], 19, 'relu', 'softmax')
model.build_model()

# Setting learning rate
model.learning_rate = 0.01
model.metrics = ["accuracy", "val_accuracy"]

# Building and compiling
model.build_optimiser()
model.compile_model()
model.build_checkpoint()

# Generating a set of training data
train_x = [[i] for i in range(0, 5)]
train_y = [[i] for i in range(0, 5)]
validate_x = [[i] for i in range(0, 2)]
validate_y = [[i] for i in range(0, 2)]

# Training model
model.train(train_x, validate_x, train_y, validate_y, 2)

