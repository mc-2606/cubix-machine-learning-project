# Imports
from os import getcwd, listdir, makedirs, path
from network.train import get_batch_split, create_load_model, create_new_model, initial_test_batch, train_model, setup_new_model, setup_load_model
from argparse import ArgumentParser
from sys import exit

# Global paths
PARENT_PATH = getcwd()
DATASET_PATH =  f"{PARENT_PATH}/machine_learning/dataset_gen/datasets"
DEFAULT_CHECKPOINTS_DIR = f"{PARENT_PATH}/machine_learning/network/checkpoints"
DEFAULT_RESULTS_DIR = f"{PARENT_PATH}/machine_learning/network/checkpoints"

# Global model constants that will probably never change
DEFAULT_INPUT_NEURON_COUNT = 54
DEFAULT_OUPTUT_NEURON_COUNT = 19
DEFAULT_HIDDEN_ACTIVATION_FUNC = 'relu'
DEFAULT_OUTPUT_ACTIVATION_FUNC = 'softmax'


# Creating the argument parser
arg_parser = ArgumentParser()

# Creating args for 2 different run modes
arg_parser.add_argument('-t', '--test', help="test or application mode", default=0)
arg_parser.add_argument('-r', '--run', help="runs and creates a new model", default=0)

# Configures the model variables
arg_parser.add_argument('-lfc', '--lfromloc', help="the name of save to be loaded")
arg_parser.add_argument('-s', '--sname', help="sets the save name of a run", default=None)
arg_parser.add_argument('-fn', '--fnumber', help="file number for files")
arg_parser.add_argument('-ts', '--tsamples', help="the amount of training samples passed through", default=10000)
arg_parser.add_argument('-lr', '--lrate', help="defines learning rate of model", default=0.01)
arg_parser.add_argument('-e', '--epoch', help="defines the amount of epochs", default=3)
arg_parser.add_argument('-ls', '--lsizes', help="defines the neuron count/size of each layer")
arg_parser.add_argument('-hlc', '--hlayercount', help="defines the amount of hidden + input layers")

# May help when seeing what files to load etc.
arg_parser.add_argument('-sh', '--showsaves', help="lists all the saves/checkpoints", default=0)


# Main run line
if __name__ == '__main__':
    args = arg_parser.parse_args()

    # Lists out the checkpoints files
    if int(args.showsaves):
        # Iterating over directories
        for save in listdir(DEFAULT_CHECKPOINTS_DIR):
            # Printing the name of directory
            print(f"[-] {save}")
        
        exit(0)
    
    # Runs a training test sample
    if int(args.test):
        # Fetching amount of training samples
        training_samples = int(args.tsamples)

        try:
            # Validating training samples exist
            if int(training_samples) < 1 or int(training_samples) > 10000:
                print("Training samples range from 1 to 10000 inclusive")
                exit(0)

            # Forces user to try again
        except Exception as error:
            print(f"{error}\nPlease try running the program again with valid data")
            exit(0)


        # Running the initial test batch
        initial_test_batch(training_samples=training_samples,
                           dataset_path=DATASET_PATH)
        exit(0)
    
    # Running training process
    if int(args.run):

        # Fetching main arguments
        save_name = args.sname
        file_no = args.fnumber
        training_samples = args.tsamples
        hidden_layer_count = args.hlayercount
        epochs = args.epoch
        learning_rate = args.lrate
        layer_sizes = None

        # Load arguments
        load_from_name = args.lfromloc
        save_name = args.sname

        # Checking if entered data is valid
        try:
            # Validating training samples exist
            if int(training_samples) < 1 or int(training_samples) > 10000:
                print("Training samples range from 1 to 10000 inclusive!")
                exit(0)
            
            # Validating file exists 
            if int(file_no) < 1 or int(file_no) > 10:
                print("There are only 10 sets of training data [1 - 10]!")
                exit(0)
            
            # Validating epoch count
            if int(epochs) < 1:
                print("You must have a valid number of epochs!")
                exit(0)
            
            # Validating learning rate
            if float(learning_rate) > 1:
                print("For machine learning, results are generally better with smaller learning rates!")
                exit(0)

            # Creating new save location
            save_location = DEFAULT_CHECKPOINTS_DIR + f"/{save_name}"
            makedirs(save_location)

        # Forces user to try again
        except Exception as error:
            print(f"{error}\nPlease try running the program again with valid data")
            exit(0)

        # Generating batches
        batches = get_batch_split(dataset_path=DATASET_PATH,
                                  file_no=file_no,
                                  training_samples=training_samples)

        # Reference model
        model = None

        # Determines whether to create or run a new model 
        if load_from_name is None:

            # Getting neuron count
            layer_sizes = (args.lsizes).split(',')
            layer_sizes = [int(layer_size) for layer_size in layer_sizes]

            # Creating a new model
            model = create_new_model(
                checkpoint_path=DEFAULT_CHECKPOINTS_DIR,
                hidden_layer_count=hidden_layer_count,
                layer_sizes=layer_sizes,
                output_neuron_count=DEFAULT_OUPTUT_NEURON_COUNT,
                hidden_activation_func=DEFAULT_HIDDEN_ACTIVATION_FUNC,
                output_activation_func=DEFAULT_OUTPUT_ACTIVATION_FUNC,
                to_save_name=save_name,
                learning_rate=learning_rate
                )

            # Setting up the new model
            setup_new_model(model)
        
        else:
            # If the loading location exists
            if path.exists(f"{DEFAULT_CHECKPOINTS_DIR}/{str(load_from_name)}"):

                # Loads the model
                model = create_load_model(
                    checkpoint_path=DEFAULT_CHECKPOINTS_DIR,
                    load_from_name=load_from_name,
                    to_save_name=save_name
                    )
                
                # Settings up the loaded model
                setup_load_model(model)
            
            # If the loading path does not exist
            else:
                print("Please load from a valid checkpoint location\n   use -sh 1 to list out the available checkpoints")
                exit(0)
        
        # Training the model
        train_model(model=model,
                    features_train=batches[0],
                    features_val=batches[1],
                    labels_train=batches[2],
                    labels_val=batches[3],
                    epochs=epochs)

        exit(0)
