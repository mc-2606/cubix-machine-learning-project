# Module imports imports
from cv2 import VideoCapture
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage

# Importing other important modules
from packages.modules.scan import convertimage_qt

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
                # Emitting the image
                converted_image = convertimage_qt(frame)
                self.image_update.emit(converted_image)

            # If no camera present
            else:
                raise Exception("[ERROR] Cannot locate camera video device")

    # To stop thread process omgg slay
    def stop(self):
        self.thread_active = False
        self.quit()


# The scan window
class ScanWindow(QWidget):
    # OOP inheritance from QMainWindow
    def __init__(self):
        super(ScanWindow, self).__init__()

        self.SCAN_ORDER = [
            "White",
            "Red",
            "Green",
            "Orange",
            "Blue",
            "Yellow"
        ]

        # Setting out main widgets
        self.layout = QVBoxLayout()
        self.view_finder = QLabel()
        self.scan_side = QLabel()

        # Allow permission button
        self.permission_button = QPushButton()
        self.permission_button.setText("Allow permission")
        self.permission_button.clicked.connect(self.allow_camera_permission)

        # Do not allow permission button
        self.no_permission_button = QPushButton()
        self.no_permission_button.setText("No permission")
        self.no_permission_button.clicked.connect(self.no_camera_permission)

        # Permission Prompt
        self.permission_prompt = QLabel()
        self.permission_prompt.setText("Request permission to use camera")

        # Which side to currently scan + scanned sides
        self.current_scan = 0
        self.current_side = QLabel()
        self.current_side.setText("Scan: " + self.SCAN_ORDER[self.current_scan])
        
        self.scanned = "Scanned sides: "
        self.scanned_sides = QLabel()
        self.scanned_sides.setText(self.scanned)
        
        # The image thread -> outputs are fed into the view_finder
        self.image_thread = ImageThread()
    
    # Updates the scanned sides
    def increment_scan(self):
        # Whilst the scans are less than 6 (comparing the index)
        if self.current_scan < 5:
            # Incrementing scan
            self.current_scan += 1

            # Updating variables
            side = "Scan: " + self.SCAN_ORDER[self.current_scan]
            self.scanned += (", " + side)

            # Updating widget text
            self.current_side.setText(side)
            self.scanned_sides.setText(self.scanned) 
    
    # Feeds the image to view_finder to be displayed
    def update_fiewfinder(self, image):
        image = QPixmap.fromImage(image)
        self.view_finder.setPixmap(image)
    
    # Starts the threading process
    def start_viewfinder_thread(self):
        self.image_thread.start()
        self.image_thread.image_update.connect(self.update_fiewfinder)
    
    # Removing startup widgets
    def remove_application_startup(self):
        self.permission_prompt.setParent(None)
        self.permission_button.setParent(None)
        self.no_permission_button.setParent(None)
    
    # Adding startup widgets
    def application_startup(self):
        # Adding widgets
        self.layout.addWidget(self.permission_prompt)
        self.layout.addWidget(self.permission_button)
        self.layout.addWidget(self.no_permission_button)

        # Setting out the app configs
        self.setLayout(self.layout)
        self.setWindowTitle("CUBIX")
    
    # Adds the scan widgets
    def add_scan_widgets(self):
        # Adding widgets
        self.layout.addWidget(self.current_side)
        self.layout.addWidget(self.scanned_sides)
        self.layout.addWidget(self.view_finder)
    
    # When permission to use camera allowed
    def allow_camera_permission(self):
        # Removing prompts and adding camera threads
        self.start_viewfinder_thread()
        self.remove_application_startup()
        self.add_scan_widgets()
        
    # When permission is not allowed
    def no_camera_permission(self):
        # Creating message window
        message = QMessageBox()
        message.setText("Important")
        message.setInformativeText("You need to use a camera for this application!")

        message.exec()
