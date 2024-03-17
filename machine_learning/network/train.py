# Imports
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from .model import Model


# Constants
SOLVED_TOKEN = '$'


# Label encoding
LABELS = ["F", "R", "U", "L", "B", "D", "F'", "R'", "U'", "L'", "B'", "D'", "F2", "R2", "U2", "L2", "B2", "D2", "S"]

# Initialise the encoder
label_encoder = LabelEncoder()
label_encoder.fit(LABELS)


# Returns a list of the input data
def format_file(filename:str, limit=8):

    # The new values to be returned
    out_vals = []

    # Current solve count
    solve_count = 0
   
    # Opening and returning file
    with open(filename, 'r+') as file:
        # Iterating over file
        for line in file:
            
            # Geting right amount of solves
            if solve_count < limit:
                # Indication of a new line
                if str(line) == SOLVED_TOKEN + "\n":
                    solve_count += 1
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
def load_training_data(dataset_path:str, file_no:int, limit=100):
    # Gathers the required file names
    target_scramble = f"{dataset_path}/scramble{file_no}.txt"
    target_solutions = f"{dataset_path}/solutions{file_no}.txt"
    
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
    # Using sklearn to split up the data
    x_train, x_val, y_train, y_val = train_test_split(features, labels, test_size=valid_size)

    # Returning the training and validation data
    return x_train, x_val, y_train, y_val

# Encodes the labels into numerical integers
def label_encode(target:list):
    # Transforming and replacing the order 
    encoded_data = label_encoder.transform(target)
    
    # Converting each item (previously numpy.int32) to python integer
    data = [int(label) for label in encoded_data]

    # Returning encoded data
    return data


# Splits up the data into features and labels for training and validating
def get_batch_split(dataset_path, file_no, training_samples):
    # Splitting up data into training and validating batches
    batch = load_training_data(dataset_path=dataset_path, file_no=int(file_no), limit=int(training_samples))
    split_batch = split_train_valid(batch[0], batch[1], 0.3, 69)
    
    # Splitting up batch into features and labels
    features_train = split_batch[0]
    features_val = split_batch[1]
    labels_train = label_encode(split_batch[2])
    labels_val = label_encode(split_batch[3])

    # Returning features + labels
    return features_train, features_val, labels_train, labels_val


# Creates a model for loading
def create_load_model(checkpoint_path, load_from_name, to_save_name):

    # Creating the model
    model = Model(checkpoint_path=checkpoint_path,
                  load_from_name=load_from_name,
                  to_save_name=to_save_name)

    # Returning the model
    return model

# Creates a new model from scratch
def create_new_model(checkpoint_path, hidden_layer_count, layer_sizes, output_neuron_count, hidden_activation_func, output_activation_func, to_save_name, learning_rate):

    # Creating a new model with args
    model = Model(
        checkpoint_path=checkpoint_path,
        layer_sizes=layer_sizes,
        hidden_layer_count=int(hidden_layer_count),
        output_neuron_count=int(output_neuron_count),
        hidden_activation_func=hidden_activation_func,
        output_activation_func=output_activation_func,
        to_save_name=to_save_name,
        learning_rate=float(learning_rate)
    )

    # Returning the model
    return model

# Function to handle a new model
def setup_new_model(model:Model):
    # Building training properties for the model
    model.build_model()
    model.build_optimiser()
    model.build_checkpoint()

    # Compiling and saving the model
    model.compile_model()
    model.log_model_variables()

# Function to handle model when loading
def setup_load_model(model:Model):
    # Loading + Building model
    model.load_model_variables()
    model.build_model()
    model.load_model()
    
    # Compiling and saving the model
    model.build_optimiser()
    model.build_checkpoint()
    model.compile_model()
    model.log_model_variables()


def train_model(model:Model, features_train, features_val, labels_train, labels_val, epochs):

    # Training the model
    evals = model.train(
        features_train=features_train,
        features_validate=features_val,
        labels_train=labels_train,
        labels_validate=labels_val,
        epochs=int(epochs)
    )

    # Plotting the model
    model.plot_history(evals)


# Function for the first initial test (batch)
def initial_test_batch(training_samples:int, dataset_path:str):
    # Splitting up data into training and validating batches
    batch = load_training_data(dataset_path=dataset_path, file_no=1, limit=training_samples)
    split_batch = split_train_valid(batch[0], batch[1], 0.3, 69)
    
    # Splitting up batch into features and labels
    features_train = split_batch[0]
    features_val = split_batch[1]
    labels_train = label_encode(split_batch[2])
    labels_val = label_encode(split_batch[3])

    # Creating the model
    model = Model(hidden_layer_count=4, 
              layer_sizes=[54, 1024, 2048, 1024],
              output_neuron_count=19,
              hidden_activation_func='relu',
              output_activation_func='softmax', 
              metrics=['accuracy', 'val_accuracy'],
              learning_rate=0.0003)
    
    # Initialising model
    model.build_model()
    model.build_optimiser()
    #model.build_checkpoint()
    model.compile_model()

    # Training model + getting results
    evals = model.train(features_train, features_val, labels_train, labels_val, epochs=3)
    model.plot_history(evals)

def train_modelSSS(hidden_layer_count:int, neuron_count:list, output_neuron_count:int, hidden_activation_func:str, output_activation_func:str, epochs:int, training_samples:int, file_no:int, ckpt_path:str, model_load:bool):
    # Splitting up data into training and validating batches
    batch = load_training_data(file_no=file_no, limit=training_samples)
    split_batch = split_train_valid(batch[0], batch[1], 0.3, 69)
    
    # Splitting up batch into features and labels
    features_train = split_batch[0]
    features_val = split_batch[1]
    labels_train = label_encode(split_batch[2])
    labels_val = label_encode(split_batch[3])

    # Creating the model
    model = Model(hidden_layer_count=hidden_layer_count, 
              layer_sizes=neuron_count,
              output_neuron_count=output_neuron_count,
              hidden_activation_func=hidden_activation_func,
              output_activation_func=output_activation_func, 
              metrics=['accuracy', 'val_accuracy'],
              learning_rate=0.0003)
    
    # Initialising model
    model.build_model()
    
    # Loading the model
    if model_load:
        model.load_model(f"{ckpt_path}.ckpt")
    
    model.build_checkpoint()
    model.compile_model()

    # Training model + getting results
    evals = model.train(features_train, features_val, labels_train, labels_val, epochs=epochs)
    model.plot_history(evals)



features, labels = load_training_data("C:\project\project\machine_learning\dataset_gen\datasets/", 1, limit=5)
split_data = split_train_valid(features, labels, 0.2, 1)

