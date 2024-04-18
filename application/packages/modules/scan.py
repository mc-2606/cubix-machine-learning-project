# Module imports
from numpy import uint8
from cv2 import cvtColor, COLOR_BGR2RGB, COLOR_BGR2HSV, flip, rectangle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

# Display RGB vals
COLOUR_TO_RGB = {
    'red'    : (255, 0, 0),
    'orange' : (255, 165, 0),
    'blue'   : (0, 0, 255),
    'green'  : (0, 255, 0),
    'white'  : (255, 255, 255),
    'yellow' : (255, 255, 0) 
}

# Corresponding sides for scanning
CORRESPONDING_SIDES = {
    'white': {
        'top': 'green',
        'bottom': 'blue',
        'left': 'red',
        'right': 'orange'
    },
    'red': {
        'top': 'yellow',
        'bottom': 'white',
        'left': 'blue',
        'right': 'green'
    },
    'green': {
        'top': 'yellow',
        'bottom': 'white',
        'left': 'red',
        'right': 'orange'
    },
    'orange': {
        'top': 'yellow',
        'bottom': 'white',
        'left': 'green',
        'right': 'blue'
    },
    'blue': {
        'top': 'yellow',
        'bottom': 'white',
        'left': 'orange',
        'right': 'red'
    },
    'yellow': {
        'top': 'blue',
        'bottom': 'green',
        'left': 'red',
        'right': 'orange'
    }
}


# How far apart grid spaces should be
GRID_SPACING = 120
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

        # Classifying the colour and adding to the list
        classified_colour = classify_colour(hsv_colour)        
        classified_colours.append(classified_colour)

    # Returning the classified colour
    return classified_colours

# Classifies the colour within a range
def classify_colour(hsv_colour):
    # Splitting up hsv colour into hue, saturation and value
    hue = hsv_colour[0]
    sat = hsv_colour[1]
    val = hsv_colour[2]

    # Making the colour comparisons
    if (0 <= hue < 5 or 170 <= hue <= 180) and sat > 100 and val > 100:
        return 'red'
    elif 5 <= hue < 20 and sat > 100 and val > 100:
        return 'orange'
    elif 30 <= hue < 50 and sat > 100 and val > 100:
        return 'yellow'
    elif 50 <= hue < 90 and sat > 100 and val > 100:
        return 'green'
    elif 90 <= hue < 140 and sat > 100 and val > 100:
        return 'blue'
    else:
        return 'white'

# Returns the RGB value for a colour (on a Rubik's cube)
def conv_colour_to_RGB(target_colour):

    # Iterating over the colours
    for colour in COLOUR_TO_RGB.keys():

        # If colours match, returns the RGB value for that colour
        if target_colour == colour:
            return COLOUR_TO_RGB[colour]

