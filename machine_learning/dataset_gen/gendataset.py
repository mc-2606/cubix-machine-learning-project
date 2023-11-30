# Pycuber imports
from pycuber import Cube, Formula
from pycuber.solver import CFOPSolver

# Using multiprocessing as performance is considerably better
from multiprocessing import Process
import datetime

SOLVED_TOKEN = "S"
NEW_TOKEN = "$"

numVals = {
    "white": 0,
    "red": 1,
    "green": 2,
    "orange": 3,
    "blue": 4,
    "yellow": 5
}

SOLUTIONS_NUMBER = 10000


def convertColoursToNums(cube:list):
    numsCube = [i[0] for i in cube]

    for count, colour in enumerate(cube):
        numsCube[count] = numVals[colour]
    
    return numsCube

def orderColourCube(cube:Cube):
    orderedColourCube = []

    for colour in numVals.keys():
        colourCode = cube.which_face(colour)
        colourVals = cube.get_face(colourCode)

        for firstLayer in colourVals:
            for square in firstLayer:
                orderedColourCube.append(square.colour)
    
    return orderedColourCube

def constructValidCube(cube:Cube):
    colourCube = orderColourCube(cube)
    numsCube = convertColoursToNums(colourCube)

    out = ""

    for number in numsCube:
        out += str(number) + " "

    return out

def genRandomSolve():
    formula = Formula()
    randomAlg = formula.random()

    cube = Cube()
    cube(randomAlg)

    tempCube = Cube()
    tempCube(randomAlg)
    
    solver = CFOPSolver(cube)
    solutions = list(solver.solve())
    solutions = [str(i) for i in solutions]

    return solutions, tempCube
        
def writeToFile(path, values, newline=True):
    with open(path, "a+") as file:
        file.write(values)

        if newline:
            file.write('\n')

def generateFile(filenumber):
    solutions, tempCube = genRandomSolve()

    scrambleFile = f"scramble{filenumber}.txt"
    solutionsFile = f"solutions{filenumber}.txt"

    for move in solutions:
        writeToFile(scrambleFile, constructValidCube(tempCube))
        writeToFile(solutionsFile, move)

        tempCube(move)

    writeToFile(scrambleFile, constructValidCube(tempCube))
    writeToFile(solutionsFile, SOLVED_TOKEN)

    writeToFile(scrambleFile, NEW_TOKEN)
    writeToFile(solutionsFile, NEW_TOKEN)

def generateDataset(fileNumber):
    print(f"[{datetime.datetime.now()}] Generating dataset ~ Dataset No:{fileNumber}")

    for count in range(SOLUTIONS_NUMBER):
        generateFile(fileNumber)

    print(f"[{datetime.datetime.now()}] DATASET GENERATED ~ Dataset No:{fileNumber}")  

# Creates the amount of targetted threads/processes
def create_target_process(amount):
    processes = []
    for i in range(amount):
        processes.append(Process(target=generateDataset, args=(i+1,)))
    
    return processes
            

# Main run line
if __name__ == "__main__":
    threadCount = input("thread no: ")

    processes = create_target_process(int(threadCount))

    for process in processes:
        process.start()
