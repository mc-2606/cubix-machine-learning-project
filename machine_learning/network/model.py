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
    def __init__(self, hidden_layer_count=None, layer_sizes=None, output_neuron_count=None, hidden_activation_func=None, output_activation_func=None, metrics=None, learning_rate=None, checkpoint_path=None,to_save_name=None, load_from_name=None):
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

        # Saving Parameters
        self.checkpoint_path = checkpoint_path
        self.to_save_name = to_save_name
        self.load_from_name = load_from_name

        # The actual model/network 
        self.model = Sequential()
    
    # Logs the variables in a text file
    def log_model_variables(self):
        # Generating path
        path_name = f"{self.checkpoint_path}/{self.to_save_name}/model_var.json"

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
        with open(path_name, 'w', encoding='utf-8') as file:
            dump(to_write, file, ensure_ascii=False, indent=4)
    
    # Loads the model variables and updates model variables
    def load_model_variables(self):
        # Creaeting string JSON file
        path = str(f"{self.checkpoint_path}/{self.load_from_name}/model_var.json")

        # Opening JSON file
        with open(path, 'r+', encoding='utf-8') as file:
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
    def load_model(self):
        path = str(f"{self.checkpoint_path}/{self.load_from_name}/data_var.ckpt")
        self.model.load_weights(path)
    
    # Creates a callback checkpoint
    def build_checkpoint(self):
        # Logging checkpoint
        path_name = f"{self.checkpoint_path}/{self.to_save_name}/data_var.ckpt"
        
        # Creating the checkpoint callback
        self.checkpoint_callback = ModelCheckpoint(filepath=path_name,
                                     verbose=2, # Set on logging for testing purposes
                                     save_best_only=True,
                                     monitor="accuracy") 
        
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
        # Using sparse cross entropy loss function
        self.loss_function = SparseCategoricalCrossentropy()

        # Compiling the model with optimisers, loss and metrics
        self.model.compile(optimizer=self.optimiser,
                           loss=self.loss_function,
                           metrics="accuracy")
    
    # Training the model
    def train(self, features_train, features_validate, labels_train, labels_validate, epochs):
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        print(f"[TRAINING - {current_time}] \nEpochs: {epochs}\nLearning Rate: {self.learning_rate}\nMetrics: {self.metrics}\nSGD: {self.optimiser}")

        # Training the model with input data
        history = self.model.fit(
            x=features_train,
            y=labels_train,
            validation_data=[features_validate, labels_validate],
            epochs=epochs,
            callbacks=self.checkpoint_callback,
            validation_freq=1,
            use_multiprocessing=True,
            shuffle=True,
        )

        # Returning the history object
        return history

    def plot_history(self, history):
        # Plotting down the variables
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])

        # Setting metadata
        plt.title('Model Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['train', 'val'], loc='upper left')

        # File naming
        plt.savefig(f'{self.checkpoint_path}/{self.to_save_name}/image_var.png', bbox_inches='tight')

        # Plotting data
        plt.show()

