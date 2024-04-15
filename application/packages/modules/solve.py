from pycuber import Cube, array_to_cubies, solver
from keras.models import load_model
from os import getcwd
from random import choice
import numpy as np
from pprint import pprint

NUM_VALS = {
    "white": 0,
    "red": 1,
    "green": 2,
    "orange": 3,
    "blue": 4,
    "yellow": 5
}

PYC_NUM_VALS = {
    "red": 0,
    "yellow": 1,
    "green": 2,
    "white": 3,
    "orange": 4,
    "blue": 5
}

LABELS = ["F", "R", "U", "L", "B", "D", "F'", "R'", "U'", "L'", "B'", "D'", "F2", "R2", "U2", "L2", "B2", "D2", "S"]

MODEL_LOCATION = f"{getcwd()}/packages/modules/"
MODEL_SAVE_NAME = "running_model"

# model = create_load_model(checkpoint_path=MODEL_LOCATION, load_from_name=MODEL_SAVE_NAME)
# load_predict_model(model)


# Converting the colours to numbers
def conv_colour_to_nums(cube:list):
    # Iterating over the cube
    for count, colour in enumerate(cube):
        # Replacing each letter with corresponding number
        cube[count] = NUM_VALS[colour]
    
    # Returning the numbered cube
    return cube

# Converting the colours to numbers
def conv_colour_to_nums_pyc(cube:list):
    # Iterating over the cube
    for count, colour in enumerate(cube):
        # Replacing each letter with corresponding number
        cube[count] = NUM_VALS[colour]
    
    # Returning the numbered cube
    return cube

# Returning the cube into an ordered state (in the same orer as NUM_VALS)
def order_colour_cube(cube:Cube):
    # The cube represented as an array
    ordered_colour_cube = []

    # Going through colour
    for colour in NUM_VALS.keys():
        # Fetching the current colour
        colour_code = cube.which_face(colour)
        colour_vals = cube.get_face(colour_code)

        # Fetching the square colours
        for item in colour_vals:
            for piece in item:
                # Adding the colour of the square to the cube array
                ordered_colour_cube.append(piece.colour)
    
    # Returning the cube array
    return ordered_colour_cube

def flatten(input_list):
    output = ""

    for item in input_list:
        output += str(item)
    
    return output


def set_cube(cubie_form:list):
    cubies = array_to_cubies(cubie_form)
    cube = Cube(cubies)
    
    return cube

def process_input_array(input_list):
    # Divide the input list into sublists of size 9
    sublists = [input_list[i:i+9] for i in range(0, len(input_list), 9)]

    # Divide each sublist into nested lists of size 3
    nested_lists = [np.array([sublist[i:i+3] for i in range(0, len(sublist), 3)]) for sublist in sublists]


    for count, sublist in enumerate(nested_lists):
        nested_lists[count] = sublist.T.tolist()

    flat_list = [item for sublist in nested_lists for nested_list in sublist for item in nested_list]

    return flat_list

def solve_cube(input_array):
    # Conerting array to cubie format
    transposed_array = process_input_array(input_array)

    # Applying temporary
    print(transposed_array)
    model_array = conv_colour_to_nums_pyc(transposed_array)

    # Generating valid cube
    numbered_cube = conv_colour_to_nums(transposed_array)
    cubie_form = flatten(numbered_cube)
    py_cube = set_cube(cubie_form)

    # model_array[0:9], model_array[9:18], model_array[18:27], model_array[27:36], model_array[36:45], model_array[45:54] = transposed_array[9:18], transposed_array[45:54], transposed_array[18:27], transposed_array[0:9], transposed_array[27:36], transposed_array[36:45]


    model = load_model(MODEL_LOCATION+MODEL_SAVE_NAME+"/data_var.ckpt")

    count = 0

    while True:
        str_cube = order_colour_cube(py_cube)

        numbered_cube = conv_colour_to_nums(str_cube)
        cubie_form = flatten(numbered_cube)

        py_cube = set_cube(cubie_form)

        predicted_num = np.argmax(model.predict([numbered_cube]), axis=1)[0]
        predicted_move = LABELS[predicted_num]

        print(py_cube)

        if predicted_move == "S":
            if py_cube == Cube():
                print("cube is actually solved")
                break

            print("false solve")
        else:
            print(py_cube, predicted_move)
            py_cube(predicted_move)

        count += 1
        input()

# print(process_input_array([1, 2, 3, 4, 5, 6, 7, 8, 9]))


