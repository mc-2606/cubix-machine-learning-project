# Module imports imports
from cv2 import VideoCapture, cvtColor, COLOR_BGR2RGB, flip
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QImage


class ImageThread(QThread):
    image_update = pyqtSignal(QImage)

    # On thread.start()
    def run(self):
        self.thread_active = True

        # Capturing video
        capture = VideoCapture(0)

        while self.thread_active:
            ret, frame = capture.read()

            # If camera is present
            if ret:
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

                qt_image = qt_conv.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)

                # Emitting a 'signal' to update image_update
                self.image_update.emit(qt_image)
            
            # If no camera present
            else:
                raise Exception("[ERROR] Cannot locate camera video device")

    # To stop thread process
    def stop(self):
        self.thread_active = False
        self.quit()


# The scan window
class ScanWindow(QWidget):
    # OOP inheritance from QMainWindow
    def __init__(self):
        super(ScanWindow, self).__init__()
        
        # Setting a 'test' title
        self.setWindowTitle("CUBIX")

        # Setting out main widgets
        self.layout = QVBoxLayout()
        self.view_finder = QLabel()
        self.layout.addWidget(self.view_finder)
        
        # The image thread -> outputs are fed into the view_finder
        self.image_thread = ImageThread()
        self.image_thread.image_update.connect(self.update_fiewfinder)

        # Setting out the layout
        self.setLayout(self.layout)
    
    # Feeds the image to view_finder to be displayed
    def update_fiewfinder(self, image):
        image = QPixmap.fromImage(image)
        self.view_finder.setPixmap(image)
    
    # Starts the threading process
    def start_viewfinder_thread(self):
        self.image_thread.start()
        self.image_thread.image_update.connect(self.update_fiewfinder)

