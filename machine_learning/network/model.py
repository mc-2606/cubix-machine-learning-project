# Importing modules
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.losses import SparseCategoricalCrossentropy
from matplotlib import pyplot as plt

from datetime import datetime
from json import dump, load

# CONSTANTS
CHECKPOINT_PATH_TF = "network/checkpoints/checkpoint_files/"

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
        self.metrics = metrics
        self.learning_rate = learning_rate
        self.optimiser = None
        self.checkpoint_callback = None

        # The actual model/network 
        self.model = Sequential()
    
    # Logs the variables in a text file
    def log_model_variables(self):
        # Fetching current time and logging variables
        current_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        path_name = f"network/checkpoints/{current_time}.json"

        # The data needed to be written or saved
        to_write = {
            "hidden_layer_count": self.hidden_layer_count,
            "layer_sizes": self.layer_sizes,
            "output_neuron_count": self.output_neuron_count,
            "hidden_activation_func": self.hidden_activation_func,
            "output_activation_func": self.output_activation_func,
            "metrics": self.metrics,
            "learning_rate": self.learning_rate,
        }

        # Dumping (writing) the file
        with open(path_name, 'w+', encoding='utf-8') as file:
            dump(to_write, file, ensure_ascii=False, indent=4)
    
    # Loads the model variables and updates model variables
    def load_model_variables(self, model_file):

        # Opening JSON file
        with open(model_file, 'r+', encoding='utf-8') as file:
            consts = load(file)

            # Updating network parameters
            self.hidden_layer_count = consts["hidden_layer_count"]
            self.layer_sizes = consts["layer_sizes"]
            self.output_neuron_count = consts["output_neuron_count"]
            self.hidden_activation_func = consts["hidden_activation_func"]
            self.output_activation_func = consts["output_activation_func"]
            self.metrics = consts["metrics"]
            self.learning_rate = consts["learning_rate"]

    # Loads the targetted checkpoint_file into the model
    def load_model(self, checkpoint_file):
        self.model.load_weights(checkpoint_file)
    
    # Creates a callback checkpoint
    def build_checkpoint(self, epochs:int):
        # Fetching current time and logging variables
        current_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        path_name = f"{current_time}.ckpt"
        
        # Creating the checkpoint callback
        self.checkpoint_callback = ModelCheckpoint(filepath=path_name,
                                     verbose=1, # Set on logging for testing purposes
                                     save_best_only=True,
                                     save_freq=epochs,
                                     monitor=self.metrics) 
        
    
    # Constructs the layers into the model
    def build_model(self):
        # Adding the required input layers
        for count in range(self.hidden_layer_count):
            layer = Dense(units=(self.layer_sizes[count]), activation=self.hidden_activation_func, name=f"layer_{count}")
            self.model.add(layer)
        
        # Adding the output layer
        output_layer = Dense(units=(self.output_neuron_count), activation=self.output_activation_func, name="layer_output")
        self.model.add(output_layer)

    # The SGD (calc)
    def build_optimiser(self):
        self.optimiser = Adam(learning_rate=self.learning_rate)


    # Adding loss function
    def compile_model(self):
        self.loss_function = SparseCategoricalCrossentropy()

        self.model.compile(optimizer=self.optimiser,
                           loss=self.loss_function,
                           metrics=["accuracy",])
        
    def train(self, features_train, features_validate, labels_train, labels_validate, epochs):
        history = self.model.fit(
            x=features_train,
            y=labels_train,
            validation_data=[features_validate, labels_validate],
            epochs=epochs,
            callbacks=self.checkpoint_callback
        )

        print(history.history['accuracy'])

        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()

