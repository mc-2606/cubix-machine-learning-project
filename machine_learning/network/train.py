# Imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from model import Model

# Constants
DATASET_PATH = "dataset_gen/datasets/"
FILESIZE = 10000
EPOCHS = 3
SOLVED_TOKEN = '$'

# Network Constants
INPUT_NEURON_COUNT = 54
HIDDEN_ACTIVATION_FUNC = "relu"
OUTPUT_ACTIVATION_FUNC = "softmax"
OUTPUT_NEURONS_COUNT = 19


# Label encoding
LABELS = ["F", "R", "U", "L", "B", "D", "F'", "R'", "U'", "L'", "B'", "D'", "F2", "R2", "U2", "L2", "B2", "D2", "S"]

# Initialise the encoder
label_encoder = LabelEncoder()
label_encoder.fit(LABELS)


# Returns a list of the input data
def format_file(filename:str, limit=8):

    # The new values to be returned
    out_vals = []
   
    # Opening and returning file
    with open(filename, 'r+') as file:
        for count, line in enumerate(file):
            if count < limit:
                # Indication of a new line
                if str(line) == SOLVED_TOKEN + "\n":
                    pass
                else:
                    # Adding line to the output
                    out_vals.append(line)
            else:
                break
    
    # Returning the list
    return out_vals

# Splits up stringed items in to nested list
def format_scram_tolst(data):
    for index, state in enumerate(data):
        # Removing the the newline operator from data
        state = state[:-3]

        # Splitting up the data into
        state = state.split()
        state = [int(data) for data in state]

        # Updating the data with new format
        data[index] = state
    
    # Returning the new list
    return data

# Formats solutions
def format_sols_tolst(data):
    for index, token in enumerate(data):
        # Removes the new line space
        token = token.replace("\n", "")

        # Updating data with new format
        data[index] = token

    # Return the new list
    return data

# Loads all of the training data
def load_training_data(file_no: int, limit=100):
    # Gathers the required file names
    target_scramble = f"{DATASET_PATH}scramble{file_no}.txt"
    target_solutions = f"{DATASET_PATH}solutions{file_no}.txt"
    
    # Gathering the files
    target_scramble_data = format_file(target_scramble, limit=limit)
    target_solutions_data = format_file(target_solutions, limit=limit)

    # Ready formatted data
    format_scramble_data = format_scram_tolst(target_scramble_data)
    format_solutions_data = format_sols_tolst(target_solutions_data)
    
    # Returning correctly formatted data
    return format_scramble_data, format_solutions_data

# Splits up data into training and valid datasets
def split_train_valid(features, labels, valid_size, random_state):
    x_train, x_val, y_train, y_val = train_test_split(features, labels, test_size=valid_size, random_state=random_state)

    return x_train, x_val, y_train, y_val

# Encodes the labels into numerical integers
def label_encode(target:list):
    # Transforming and replacing the order 
    encoded_data = label_encoder.transform(target)
    
    # Converting each item (previously numpy.int32) to python integer
    data = [int(label) for label in encoded_data]

    # Returning encoded data
    return data

# Function for the first initial test (batch)
def initial_test_batch(batchsize):
    # Splitting up data into training and validating batches
    batch = load_training_data(file_no=1, limit=batchsize)
    split_batch = split_train_valid(batch[0], batch[1], 0.2, 69)
    
    # Splitting up batch into features and labels
    features_train = split_batch[0]
    features_val = split_batch[1]
    labels_train = label_encode(split_batch[2])
    labels_val = label_encode(split_batch[3])

    # Creating the model
    model = Model(hidden_layer_count=4, 
              layer_sizes=[INPUT_NEURON_COUNT, 1024, 2048, 1024],
              output_neuron_count=OUTPUT_NEURONS_COUNT,
              hidden_activation_func=HIDDEN_ACTIVATION_FUNC,
              output_activation_func=OUTPUT_ACTIVATION_FUNC, 
              metrics=['val_accuracy'],
              learning_rate=0.0003)
    
    # Initialising model
    model.build_model()
    model.build_optimiser()
    model.build_checkpoint(epochs=EPOCHS)
    model.compile_model()

    # Training model + getting results
    evals = model.train(features_train, features_val, labels_train, labels_val, epochs=EPOCHS)
    model.plot_history(evals)
