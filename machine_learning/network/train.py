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
            if count < limit:
                # Indication of a new line
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
def load_training_data(file_no: int):
    # Gathers the required file names
    target_scramble = f"{DATASET_PATH}scramble{file_no}.txt"
    target_solutions = f"{DATASET_PATH}solutions{file_no}.txt"
    
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

test1 = load_training_data(1)
test2 = split_train_valid(test1[0], test1[1], 0.2, 69)

features_train = test2[0]
features_val = test2[1]
labels_train = label_encode(test2[2])
labels_val = label_encode(test2[3])




model = Model(hidden_layer_count=4, 
              layer_sizes=[INPUT_NEURON_COUNT, 1024, 2048, 1024],
              output_neuron_count=OUTPUT_NEURONS_COUNT,
              hidden_activation_func=HIDDEN_ACTIVATION_FUNC,
              output_activation_func=OUTPUT_ACTIVATION_FUNC, 
              metrics=['val_accuracy'],
              learning_rate=0.03)

model.build_model()
model.build_optimiser()
model.build_checkpoint(epochs=EPOCHS)
model.compile_model()
model.train(features_train, features_val, labels_train, labels_val, epochs=EPOCHS)