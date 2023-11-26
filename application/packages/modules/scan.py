# Module imports
from numpy import array
from cv2 import cvtColor, COLOR_BGR2RGB, flip, inRange, rectangle, resize
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage


COLOUR_RANGES = {
    'white': {
        'lower': array([0, 0, 200]),
        'upper': array([180, 30, 255])
    },
    'red': {
        'lower': array([0, 100, 100]),
        'upper': array([10, 255, 255])
    },
    'green': {
        'lower': array([40, 100, 100]),
        'upper': array([80, 255, 255])
    },
    'orange': {
        'lower': array([10, 100, 100]),
        'upper': array([20, 255, 255])
    },
    'blue': {
        'lower': array([100, 100, 100]),
        'upper': array([140, 255, 255])
    },
    'yellow': {
        'lower': array([20, 100, 100]),
        'upper': array([30, 255, 255])
    }
}

GRID_POSITIONS = [(80, 80), (240, 80), (400, 80), (80, 240), (240, 240), (400, 240), (80, 400), (240, 400), (400, 400)]

def draw_rectangles(frame):
    for position in GRID_POSITIONS:
        rectangle(frame, (position[0] - 10, position[1] - 10), (position[0] + 10, position[1] + 10), (255, 255, 255), -1)

# Prepares image for PyQT conversion
def convertimage_qt(frame):
    # Preparing images for PyQT integration
    resize(frame, (480, 480))
    draw_rectangles(frame)
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

# Classifies the colour within a range
def classify_colour(self, colour):
    # Iterating over the specified ranges
    for colour, ranges in COLOUR_RANGES.items():
        # Getting bounds for ranges
        lower_bound = ranges['lower']
        upper_bound = ranges['upper']

        # inRange returns boolean - if the colour falls in the range
        in_range = inRange(colour, lower_bound, upper_bound)

        # If it is in range, return colour
        if in_range:
            return colour
    
    # If colour is not valid
    return None

