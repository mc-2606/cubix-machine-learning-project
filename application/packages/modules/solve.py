# Module improts
import numpy as np
from pycuber import Cube, array_to_cubies, solver, Formula
from keras.models import load_model
from os import getcwd
from sklearn.preprocessing import LabelEncoder

# Model prediction values
NUM_VALS = {
    "white": 0,
    "red": 1,
    "green": 2,
    "orange": 3,
    "blue": 4,
    "yellow": 5
}

# Representing cube with pycuber values
PYC_NUM_VALS = {
    "red": 0,
    "yellow": 1,
    "green": 2,
    "white": 3,
    "orange": 4,
    "blue": 5
}

LABELS = ["F", "R", "U", "L", "B", "D", "F'", "R'", "U'", "L'", "B'", "D'", "F2", "R2", "U2", "L2", "B2", "D2", "S"]

# The mdoel save location and the model name
MODEL_LOCATION = f"{getcwd()}/packages/modules/"
MODEL_SAVE_NAME = "model_cat_10"

MAX_PREDICTIONS = 90

# Creating a label encode for decoding predicted values
label_encoder = LabelEncoder()
label_encoder.fit(LABELS)

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

# Converting the colours to numbers
def conv_colour_to_nums(cube:list):
    # Output cube
    out_cube = []

    # Iterating over the cube
    for count, colour in enumerate(cube):
        # Replacing each letter with corresponding number
        if count < 54:
            out_cube.append(NUM_VALS[colour])

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

    # Returning the model predict array
    return numbered_cube


# Flattens the list into a formattable string
def flatten(input_list):
    # Output string
    output = ""

    # Adding the value to the string
    for item in input_list:
        output += str(item)
    
    # Returning the output
    return output

# Creating the cube
def set_cube(cubie_form):
    # Creating the cube
    cubies = array_to_cubies(cubie_form)
    cube = Cube(cubies)
    
    # Returning the cube
    return cube

# Prepares input data for pycuber format
def process_input_array(input_list):
    # Divide the input list into sublists of size 9
    sublists = [input_list[i:i+9] for i in range(0, len(input_list), 9)]

    # Divide each sublist into nested lists of size 3
    nested_lists = [np.array([sublist[i:i+3] for i in range(0, len(sublist), 3)]) for sublist in sublists]

    # Restructuring the input data
    for count, sublist in enumerate(nested_lists):
        # Transposing the face and converting it to list
        nested_lists[count] = sublist.T.tolist()

        # Mirroring the face as the scan was mirrored
        nested_lists[count] = [row[::-1] for row in nested_lists[count]]

    # Merging back sublists into 1 list
    flat_list = [item for sublist in nested_lists for nested_list in sublist for item in nested_list]
    
    # Returning the flat list
    return flat_list

# Verifying solve
def verify_solve(solutions, cube):
    # Generating the formula
    formula = Formula(solutions[:-1])

    # Checking if cube is predicted correctly
    if cube(formula) == Cube():
        return True
    return False


# Solves the cube
def solve_cube(input_array):
    # Converting array to cubie format
    pyc_array = process_input_array(input_array)

    # Swapping order for cubies
    pyc_array[0:9], pyc_array[9:18], pyc_array[18:27], pyc_array[27:36], pyc_array[36:45], pyc_array[45:54] = pyc_array[9:18], pyc_array[45:54], pyc_array[18:27], pyc_array[0:9], pyc_array[27:36], pyc_array[36:45]

    # Converting the data
    pyc_cube_array = conv_colour_to_nums_pyc(pyc_array)
    pyc_cubie_form = flatten(pyc_cube_array)
    
    # Loading the model
    model = load_model(f"{MODEL_LOCATION}{MODEL_SAVE_NAME}\data_var.ckpt")
    
    # Generating the appropriate cubes
    model_predict_cube = set_cube(pyc_cubie_form) # Cube for model prediction
    to_solve_cube = set_cube(pyc_cubie_form) # Cube for generating pycuber cube
    verify_cube = set_cube(pyc_cubie_form) # Cube for verifying the predictions are valid

    # Using pycuber to generate the actual solve
    cfop_solver = solver.CFOPSolver(to_solve_cube)
    pycuber_solutions = [str(move) for move in cfop_solver.solve()]

    # To keep track of predictions
    predicted_solutions = []
    prediction_index = 0

    # Any matching solutions to backtrack to incase of a loop
    previous_matching = True
    previous_matching_index = 0


    # Iteratively solving the cube
    while True:
        # Generating the array for model prediction
        model_predict_array = prepare_predict_array(model_predict_cube)
        
        # Getting the predicted move
        predicted_num = np.argmax(model.predict([model_predict_array]), axis=1)[0]
        predicted_move = str(label_encoder.inverse_transform([predicted_num])[0])

        # Adding the solutions to the predicted move
        predicted_solutions.append(predicted_move)

        # If the move predicted has been solved
        if predicted_move == "S" and verify_solve(predicted_solutions, verify_cube):
            return predicted_solutions
        else:
            # Reverting verify cube to original state
            verify_cube = set_cube(pyc_cubie_form)
       
        # If matching so far with the generated solutions 
        if previous_matching:
            # If predicted move matches the generated solution
            if pycuber_solutions[prediction_index] == predicted_move:
                previous_matching_index += 1
            # If the predicted move does not match the generated solution
            else:
                previous_matching = False
        
        # Backtracking (in infinite loops)
        if (predicted_move == f"{predicted_solutions[prediction_index-1]}'" or predicted_move == predicted_solutions[prediction_index-1]) and prediction_index > 0 or prediction_index > MAX_PREDICTIONS:
            # Reverting to last previously correct state
            predicted_solutions = predicted_solutions[0:previous_matching_index]
            prediction_index = previous_matching_index

            # Fetching the next predicted move
            next_correct_move = str(pycuber_solutions[previous_matching_index])

            # Reverting cube to previous matching state
            model_predict_cube = set_cube(pyc_cubie_form)
            model_predict_cube(predicted_solutions)

            # Pycuber converts the moves into steps so we need to convert them back to strings
            predicted_solutions = [str(move) for move in predicted_solutions]

            # Applying the next correct move to the cubes
            model_predict_cube(next_correct_move)
            predicted_solutions.append(next_correct_move)

            # Updating indexes and now the predictions should match the solutions up to a point
            prediction_index += 1
            previous_matching_index += 1
            previous_matching = True

        else:
            # If a different move, then just applying the move
            model_predict_cube(predicted_move)
            prediction_index += 1
        
        print(model_predict_cube)
        print(predicted_solutions)
        print(pycuber_solutions)
