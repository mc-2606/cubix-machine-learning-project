# Imports
from os import getcwd, listdir, makedirs
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
arg_parser.add_argument('-lc', '--lchecks', help="lists all checkpoints", default=0)
arg_parser.add_argument('-lir', '--lres', help="lists all image results", default=0)
arg_parser.add_argument('-lm', '-lmodel', help="lists all model variables", default=0)

if __name__ == '__main__':
    args = arg_parser.parse_args()

    # Lists out the checkpoints files
    if int(args.lchecks):
        for file in listdir(DEFAULT_CHECKPOINTS_DIR):
            print(file)
        exit(0)
    
    # Lists the checkpoint files
    if int(args.lres):
        for file in listdir(DEFAULT_RESULTS_DIR):
            if file == "checkpoint_files":
                pass
            print(file)
        exit(0)
    
    # Runs a training test sample
    if int(args.test):
        # Fetching amount of training samples
        training_samples = int(args.tsamples)

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

        # Checking to see if save location is available (no duplicates)
        try:
            # Creating new save location
            save_location = DEFAULT_CHECKPOINTS_DIR + f"/{save_name}"
            makedirs(save_location)
        
        # Forces user to try again
        except Exception as error:
            print(f"{error}\nPlease try again")
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

            setup_new_model(model)
        
        else:
            # Loads the model
            model = create_load_model(
                checkpoint_path=DEFAULT_CHECKPOINTS_DIR,
                load_from_name=load_from_name,
                to_save_name=save_name
                )
            
            setup_load_model(model)
        
        # Training the model
        train_model(model=model,
                    features_train=batches[0],
                    features_val=batches[1],
                    labels_train=batches[2],
                    labels_val=batches[3],
                    epochs=epochs)

        exit(0)
    