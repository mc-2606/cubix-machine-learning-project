# Importing modules
from keras.models import Sequential
from keras.layers import Input, Dense


# Network Constants
HIDDEN_ACTIVATION_FUNC = "relu"
OUTPUT_ACTIVATION_FUNC = "soft-max"
OUTPUT_NEURONS_COUNT = 19


# Creating the model + layers
def build_model(hidden_layer_count:int, layer_sizes:list):
    # Creating model
    model = Sequential()

    # Adding the required input layers
    for count in hidden_layer_count:
        layer = Dense(shape=(layer_sizes[count]), activation=HIDDEN_ACTIVATION_FUNC)
        model.add(layer)
    
    # Adding the output layer
    output_layer = Dense(shape=(OUTPUT_NEURONS_COUNT), activation=OUTPUT_ACTIVATION_FUNC)
    model.add(output_layer)

    # Returning the model
    return model
