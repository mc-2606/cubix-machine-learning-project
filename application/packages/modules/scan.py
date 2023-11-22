# Module imports
from cv2 import cvtColor, COLOR_BGR2RGB, flip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage


# Prepares image for PyQT conversion
def convertimage_qt(frame):
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

# Classifies the colour within a range
def classify_colour(self, colour):
    pass