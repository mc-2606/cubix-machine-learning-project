from pycuber import Cube, array_to_cubies, solver
from keras.models import load_model
from os import getcwd
import numpy as np


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
MODEL_SAVE_NAME = "test_run"


# Converting the colours to numbers
def conv_colour_to_nums(cube:list):
    out_cube = []

    # Iterating over the cube
    for count, colour in enumerate(cube):
        # Replacing each letter with corresponding number
        if count < 54:
            out_cube.append(NUM_VALS[colour])

            count += 1
    return out_cube

# Converting the colours to numbers
def conv_colour_to_nums_pyc(cube:list):
    out_cube = []

    # Iterating over the cube
    for count, colour in enumerate(cube):
        # Replacing each letter with corresponding number
        if count < 54:
            out_cube.append(PYC_NUM_VALS[colour])

            count += 1
    
    # Returning the numbered cube
    return out_cube

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

# Constructing the cube into a text format for writing
def prepare_predict_array(cube:Cube):
    # Converting the cube to an ordered numbered cube
    coloured_cube = order_colour_cube(cube)
    numbered_cube = conv_colour_to_nums(coloured_cube)

    return numbered_cube


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
    print(cubie_form)
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

# Solves the cube
def solve_cube(input_array):
    # Converting array to cubie format
    pyc_array = process_input_array(input_array)

    # Swapping order for cubies
    pyc_array[0:9], pyc_array[9:18], pyc_array[18:27], pyc_array[27:36], pyc_array[36:45], pyc_array[45:54] = pyc_array[9:18], pyc_array[45:54], pyc_array[18:27], pyc_array[0:9], pyc_array[27:36], pyc_array[36:45]

    # Applying temporary
    pyc_cube_array = conv_colour_to_nums_pyc(pyc_array)
    pyc_flatten_array = flatten(pyc_cube_array)

    # Generating the pycuber cube
    py_cube = set_cube(pyc_flatten_array)

    # Loading the model
    model = load_model(f"{MODEL_LOCATION}{MODEL_SAVE_NAME}\data_var.ckpt")

    count = 0

    # Using pycuber to generate the actual solve
    cfop_solver = solver.CFOPSolver(py_cube)
    solve = [str(i) for i in cfop_solver.solve()]

    print(solve)

    print(py_cube)

    while True:
        model_predict_array = prepare_predict_array(py_cube)

        predicted_num = np.argmax(model.predict([model_predict_array]), axis=1)[0]
        predicted_move = LABELS[predicted_num]

        if predicted_move == "S":
            if py_cube == Cube():
                print("cube is actually solved")
                break

            print("false solve")
        else:
            py_cube(predicted_move)
            print(py_cube, predicted_move)
            

        count += 1
        input()

