# Imports
from os import getcwd, listdir
from network.train import initial_test_batch, train_model
from argparse import ArgumentParser
from sys import exit

# Global paths
PARENT_PATH = getcwd()
DATASET_PATH =  f"{PARENT_PATH}/machine_learning/dataset_gen/datasets"
DEFAULT_CHECKPOINTS_DIR = f"{PARENT_PATH}/machine_learning/network/checkpoint/checkpoint_files"
DEFAULT_RESULTS_DIR = "{PARENT_PATH}/machine_learning/network/checkpoint"

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
arg_parser.add_argument('-c', '--ckptloc', help="sets the model to be loaded/run to", default=None)
arg_parser.add_argument('-fn', '--fnumber', help="file number for files")
arg_parser.add_argument('-ts', '--tsamples', help="the amount of training samples passed through", default=10000)
arg_parser.add_argument('-lr', '--lrate', help="defines learning rate of model", default=0.01)
arg_parser.add_argument('-e', '--epoch', help="defines the amount of epochs", default=3)
arg_parser.add_argument('-nc', '--ncount', help="defines the neurone count of each layer")
arg_parser.add_argument('-hlc', '--hlayercount', help="defines the amount of hidden + input layers")

# May help when seeing what files to load etc.
arg_parser.add_argument('-lc', '--lchecks', help="lists all checkpoints", default=0)
arg_parser.add_argument('-lir', '--lres', help="lists all image results", default=0)
arg_parser.add_argument('-lm', '-lmodel', help="lists all model variables", default=0)

if __name__ == '__main__':
    args = arg_parser.parse_args()

    if int(args.lchecks):
        for file in listdir(DEFAULT_CHECKPOINTS_DIR):
            print(file)
        exit(0)
    
    if int(args.lres):
        for file in listdir(DEFAULT_RESULTS_DIR):
            if file == "checkpoint_files":
                pass
            print(file)
        exit(0)
    
    if int(args.test):
        training_samples = int(args.tsamples)
        initial_test_batch(training_samples=training_samples,
                           dataset_path=DATASET_PATH)
        exit(0)
    
    if int(args.run):
        ckpt_file = args.ckpt_loc
        file_no = int(args.fnumber)
        training_samples = int(args.tsamples)
        hidden_layer_count = int(args.hlayercount)
        epochs = int(args.epochs)

        neuron_count = (args.ncount).split(',')
        neuron_count = [int(neuron) for neuron in neuron_count]
        
        model_load = True
        
        if ckpt_file is None:
            model_load = False

        train_model(training_samples=training_samples,
                    neuron_count=neuron_count,
                    output_neuron_count=DEFAULT_OUPTUT_NEURON_COUNT,
                    hidden_activation_func=DEFAULT_HIDDEN_ACTIVATION_FUNC,
                    output_activation_func=DEFAULT_OUTPUT_ACTIVATION_FUNC,
                    epochs=epochs,
                    hidden_layer_count=hidden_layer_count,
                    file_no=file_no,
                    ckpt_loc=ckpt_file,
                    model_load=model_load)
        
        exit(0)
    