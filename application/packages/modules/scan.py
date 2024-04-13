# Module imports
from numpy import array, uint8
from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_BGR2HSV, flip, inRange, rectangle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

COLOUR_RANGES = {
    'white': {'lower': array([0, 0, 180]), 'upper': array([30, 30, 255])},  # Hue: 0-30, Saturation: 0-30, Value: 180-255
    'red': {'lower': array([0, 100, 100]), 'upper': array([10, 255, 255])},  # Hue: 0-10, Saturation: 100-255, Value: 100-255
    'green': {'lower': array([40, 100, 100]), 'upper': array([80, 255, 255])},  # Hue: 40-80, Saturation: 100-255, Value: 100-255
    'orange': {'lower': array([10, 100, 100]), 'upper': array([25, 255, 255])},  # Hue: 10-25, Saturation: 100-255, Value: 100-255
    'blue': {'lower': array([100, 100, 100]), 'upper': array([130, 255, 255])},  # Hue: 100-130, Saturation: 100-255, Value: 100-255
    'yellow': {'lower': array([20, 100, 100]), 'upper': array([40, 255, 255])}  # Hue: 20-40, Saturation: 100-255, Value: 100-255
}

# How far apart grid spaces should be
GRID_SPACING = 160
RECT_WIDTH = 10
RECT_COLOUR = (255, 255, 255)


# Draws the rectangles onto the frame
def draw_rectangles(frame, grid_positions):
    # Iterating over grid positions
    for position in grid_positions:

        # Adding 10 px to the top left/right of the positions as rectangle draws from corner points
        rectangle(frame,
                  (position[0] - RECT_WIDTH, position[1] - RECT_WIDTH),
                  (position[0] + RECT_WIDTH, position[1] + RECT_WIDTH),
                  RECT_COLOUR,
                  -1)

# Generates the relative grid positions
def generate_grid_positions(width, height):
    # Getting centre positions
    centre_x = width // 2
    centre_y = height // 2

    # Grid positions
    grid_positions = []

    # Iterating 3 times, but adding i and j respective amounts of grid spacing
    for i in range(1, -2, -1):
        for j in range(-1, 2, 1):
            # Getting new grid coords
            coord_x = int(centre_x + (i * GRID_SPACING))
            coord_y = int(centre_y + (j * GRID_SPACING))
            
            # Adding to grid positions
            grid_positions.append((coord_x, coord_y))
    
    # Returning grid 
    return grid_positions

# Prepares image for PyQT conversion
def convertimage_qt(frame, grid_positions):
    # Drawing grids
    draw_rectangles(frame, grid_positions)

    # Preparing images for PyQT integration
    image = cvtColor(frame, COLOR_BGR2RGB)
    flipped_image = flip(image, 1)

    # Formatting metadata
    image_data = flipped_image.data
    width = flipped_image.shape[1]
    height = flipped_image.shape[0]
    
    # Image conversion
    qt_conv = QImage(image_data,
                        width,
                        height,
                        QImage.Format.Format_RGB888)
    qt_image = qt_conv.scaled(480, 480, Qt.AspectRatioMode.KeepAspectRatio)

    # Returning converted image
    return qt_image


# Gets the colours of each grid position
def get_colours_from_grids(frame, grid_positions):
    # The classified colours
    classified_colours = []

    # Iterating over the colours
    for position in grid_positions:
        # Getting the hsv colour
        frame_colour = frame[position[1], position[0]]
        hsv_frame = cvtColor(uint8([[frame_colour]]), COLOR_BGR2HSV)
        hsv_colour = hsv_frame[0][0]

        hsv_colour = array([int(i) for i in hsv_colour])

        # Classifiying the colour and adding to the list
        classified_colour = color_detect(hsv_colour[0], hsv_colour[1], hsv_colour[2])        
        classified_colours.append(classified_colour)

    # Returning the classified colour
    return classified_colours

def color_detect(h,s,v):
    # print(h,s,v)
    if h < 5 and s>5 :
        return 'red'
    elif h <10 and h>=3:
        return 'orange'
    elif h <= 25 and h>10:
        return 'yellow'
    elif h>=70 and h<= 85 and s>100 and v<180:
        return 'green'
    elif h <= 130 and s>70:
        return 'blue'
    elif h <= 100 and s<10 and v<200:
        return 'white'

    return 'white'

# Classifies the colour within a range
def classify_colour(hsv_colour):
    # Iterating over the specified ranges
    for colour, ranges in COLOUR_RANGES.items():
        # Getting bounds for ranges
        lower_bound = ranges['lower']
        upper_bound = ranges['upper']

        # inRange returns boolean - if the colour falls in the range
        in_range = inRange(hsv_colour, lower_bound, upper_bound)

        # If it is in range, return colour
        if in_range.any():
            return colour
    
    # If colour is not valid
    return None

