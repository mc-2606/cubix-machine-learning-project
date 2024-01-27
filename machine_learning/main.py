
from os import getcwd
from network.train import Model, load_training_data, split_train_valid
from argparse import ArgumentParser

PARENT_PATH = getcwd().replace("\\", "/")
DATASET_PATH =  f"{PARENT_PATH}/machine_learning/dataset_gen/datasets"

# Loading test data
test_loaded = load_training_data(DATASET_PATH, 1)
split_data = split_train_valid(test_loaded[0], test_loaded[1], 0.2, 69)

# Splitting up data to features and labels
features_train = split_data[0]
features_val = split_data[1]
labels_train = split_data[2]
labels_val = split_data[3]

model = Model(hidden_layer_count=4, 
              layer_sizes=[54, 1024, 2048, 1024],
              output_neuron_count=19,
              hidden_activation_func="relu",
              output_activation_func="softmax", 
              metrics=['val_accuracy'],
              learning_rate=0.03)

model.build_model()
model.build_optimiser()
model.compile_model()
model.train(features_train,
            features_val,
            labels_train,
            labels_val,
            3)
