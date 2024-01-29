# Imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from .model import Model


# Constants
FILESIZE = 10000
EPOCHS = 3
SOLVED_TOKEN = '$'

# Network Constants
INPUT_NEURON_COUNT = 54
HIDDEN_ACTIVATION_FUNC = "relu"
OUTPUT_ACTIVATION_FUNC = "softmax"
OUTPUT_NEURONS_COUNT = 19


LABELS = ["F", "R", "U", "L", "B", "D", "F'", "R'", "U'", "L'", "B'", "D'", "F2", "R2", "U2", "L2", "B2", "D2", "S"]

# Initialize the encoder
label_encoder = LabelEncoder()
label_encoder.fit(LABELS)


# Returns the training file
def format_file(filename:str, limit=8):
    out_vals = []

    # Opening and returning file
    with open(filename, 'r+') as file:
        for count, line in enumerate(file):

            # Only adding required amount
            if count < limit:
                # Not adding the solved token
                if str(line) == SOLVED_TOKEN + "\n":
                    pass
                else:
                    out_vals.append(line)
            else:
                break

    # Returning the list
    return out_vals

# Splits up stringed items in to nested list
def format_scram_tolst(data):
    for index, state in enumerate(data):
        state = state[:-3]
        state = state.split()

        state = [int(data) for data in state]

        data[index] = state

    # Returning the new array
    return data

# Formats solutions
def format_sols_tolst(data):
    for index, token in enumerate(data):
        token = token.replace("\n", "")
        data[index] = token

    return data

# Loads all of the training data
def load_training_data(dataset_path:str, file_no:int):
    # Gathers the required file names
    target_scramble = f"{dataset_path}/scramble{file_no}.txt"
    target_solutions = f"{dataset_path}/solutions{file_no}.txt"

    # Gathering the files
    target_scramble_data = format_file(target_scramble, limit=1000)
    target_solutions_data = format_file(target_solutions, limit=1000)


    # Ready formatted data
    format_scramble_data = format_scram_tolst(target_scramble_data)
    format_solutions_data = format_sols_tolst(target_solutions_data)


    # Returning files
    return format_scramble_data, format_solutions_data

# Splits up data into training and valid datasets
def split_train_valid(features, labels, valid_size, random_state):
    x_train, x_val, y_train, y_val = train_test_split(features, labels, test_size=valid_size, random_state=random_state)

    return x_train, x_val, y_train, y_val

# Encodes the labels into numerial integers
def label_encode(target:list):
    encoded_data = label_encoder.transform(target)
    data = [int(label) for label in encoded_data]

    return data
