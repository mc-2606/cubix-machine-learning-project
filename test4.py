from pycuber import Cube, Formula, array_to_cubies
from pprint import pprint

NUM_VALS = {
    "white": 0,
    "red": 1,
    "green": 2,
    "orange": 3,
    "blue": 4,
    "yellow": 5
}


form = Formula()

# test = array_to_cubies("000000000111111111222222222333333444333444444555555555")
test = array_to_cubies("000000000000000000222222222333333444333444444555555555")

"""
0 is red
1 is yellow
2 is green
3 is white
4 is orange
5 is blue
"""

# Generating cube and formula
cube = Cube()
cube('F2')
print(cube)
