# Imports
from pycuber import Cube, Formula
from pycuber.solver import CFOPSolver
from threading import Thread
from argparse import ArgumentParser

# Using multiprocessing as performance is considerably better
from multiprocessing import Process
import datetime

# Important constants
SOLVED_TOKEN = "S"
NEW_TOKEN = "$"
SOLUTIONS_NUMBER = 10
NUM_VALS = {
    "white": 0,
    "red": 1,
    "green": 2,
    "orange": 3,
    "blue": 4,
    "yellow": 5
}

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


# Converting the colours to numbers
def convert_colour_to_nums(cube:list):
       # Iterating over the cube
    for count, colour in enumerate(cube):
        # Replacing each letter with corresponding number
        cube[count] = NUM_VALS[colour]
    
    # Returning the numbered cube
    return cube


# Constructing the cube into a text format for writing
def construct_valid_cube(cube:Cube):
    # Converting the cube to an ordered numbered cube
    coloured_cube = order_colour_cube(cube)
    numbered_cube = convert_colour_to_nums(coloured_cube)

    # The info written on a single line
    write_line = ""
    
    # Adding info to the out_line
    for number in numbered_cube:
        write_line += str(number) + " "

    # Returning the write line
    return write_line

# Used to generate a random solve
def gen_random_solve():
    # Randomising a formula
    formula = Formula()
    random_alg = formula.random()

    # Creating the cube and applying the formula/scramble
    cube = Cube()
    cube(random_alg)

    # Temporary cube (i.e scramble is lost on this cube)
    temp_cube = Cube()
    temp_cube(random_alg)

    # Solving the cube
    solver = CFOPSolver(temp_cube)
    solutions = list(solver.solve())
    solutions = [str(i) for i in solutions]

    # Returning the solutions and the cube
    return solutions, cube

# Universal function to write to a text file 
def write_to_file(path, values, newline=True):
    # Opening theS path to files
    with open(path, "a+") as file:
        # Writing new values
        file.write(values)

        # If writing a new line
        if newline:
            file.write('\n')

# Generates the files
def generate_file(filenumber):
    # Getting the solutions and cube required
    solutions, temp_cube = gen_random_solve()

    # The filenames
    scramble_file = f"scramble{filenumber}.txt"
    solutions_file = f"solutions{filenumber}.txt"

    # For writing each move
    for move in solutions:
        # Cube + Move states
        write_to_file(scramble_file, construct_valid_cube(temp_cube))
        write_to_file(solutions_file, move)

        # Applying move to the temporary cube
        temp_cube(move)

    # Solved cube token
    write_to_file(scramble_file, construct_valid_cube(temp_cube))
    write_to_file(solutions_file, SOLVED_TOKEN)
    
    # Writing new token
    write_to_file(scramble_file, NEW_TOKEN)
    write_to_file(solutions_file, NEW_TOKEN)

# Used to create the dataset (thread function)
def generate_dataset(file_number):
    # Start time - has no purpose apart from supplying me with info
    print(f"[{datetime.datetime.now()}] Generating dataset ~ Dataset No:{file_number}")

    # Creating a set amount of solutions through the SOLUTIONS_NUMBER constant
    for _ in range(SOLUTIONS_NUMBER):
        generate_file(file_number)

    # End time
    print(f"[{datetime.datetime.now()}] DATASET GENERATED ~ Dataset No:{file_number}")  


# Creates the amount of targeted threads/processes
def create_target_process(amount):
    # List of threads/processes
    processes = []

    # Adding the required amount of processes
    for process_number in range(amount):
        # Creating the new process/thread
        new_process =  Process(target=generate_dataset, args=(process_number+1,))
        processes.append(new_process)
    
    # Returning the process
    return processes


# Main run line
if __name__ == "__main__":
    # If I ever need to change the amount of threads
    process_count = 10

    # Creating the target processes
    processes = create_target_process(process_count)

    # Starting each process (i.e each pair of file creation)
    for process in processes:
        process.start()

    # # Creating the argument parser
    # arg_parser = ArgumentParser()

    # # How many target files
    # arg_parser.add_argument('--process_count', help="determines how many files are generated")

    # # Parsing args and getting process count
    # args = arg_parser.parse_args()
    # process_count = int(args.process_count)

    # # Creating the target processes
    # processes = create_target_process(process_count)

    # # Starting each process (i.e each pair of file creation)
    # for process in processes:
    #     process.start()

