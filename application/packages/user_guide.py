# Module imports
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from os import getcwd


# Getting image paths
PATH = getcwd()

PERMISSION_IMAGE_PATH = f"{PATH}/packages/modules/images/permission_image.png"
SCAN_IMAGE_PATH = f"{PATH}/packages/modules/images/scan_image.png"
SOLVE_IMAGE_PATH = f"{PATH}/packages/modules/images/solve_image.png"


class UserGuideWindow(QWidget):
    proceed_scan = pyqtSignal()

    def __init__(self):
        super(UserGuideWindow, self).__init__()

        # Creating the main layout
        self.layout = QVBoxLayout()

        # Defining image labels
        self.permission_image = QLabel()
        self.scan_image = QLabel()
        self.solve_image = QLabel()

        # Updating image labels
        self.permission_image.setPixmap(QPixmap(PERMISSION_IMAGE_PATH))
        self.scan_image.setPixmap(QPixmap(SCAN_IMAGE_PATH).scaledToHeight(300))
        self.solve_image.setPixmap(QPixmap(SOLVE_IMAGE_PATH))

        # When a user has finished scanning
        self.proceed_scan_button = QPushButton()
        self.proceed_scan_button.setText("Start Scanning!")
        self.proceed_scan_button.clicked.connect(self.start_scan_page)

        # Making images look nicer
        self.permission_image.setStyleSheet("border: 2px solid black;")
        self.scan_image.setStyleSheet("border: 2px solid black;")
        self.solve_image.setStyleSheet("border: 2px solid black;")

        # The welcome label
        self.welcome_label = QLabel()
        self.welcome_label.setText("Welcome to CUBIX")
        self.welcome_label.setStyleSheet("font-size: 18pt; color: #333; font-weight: bold;")

        # Creating the additional label info
        self.permission_info_label = QLabel()
        self.permission_info_label.setText("You will first be prompted to allow the application to use your camera. Please make sure we have access to your camera - allow our application to use it by clicking on the 'Allow Permission' button.")
        self.permission_info_label.setWordWrap(True)

        self.scan_info_label = QLabel()
        self.scan_info_label.setText("When scanning make sure you are scanning the right side in the right orientation. Match the colours of the side faces to the cube. When the interactive scan cube matches your real life cube you can click on the 'Scan Side' button. If you rescrambled your cube, click on the 'New Scan' button.")
        self.scan_info_label.setWordWrap(True)
        self.scan_info_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.solve_info_label = QLabel()
        self.solve_info_label.setText("When you have scanned all sides, the program will automatically start generating the solve for you. Please be patient! If you want to start a new solve, please click on the 'New Solve' button.")
        self.solve_info_label.setWordWrap(True)

        # Setting a max size
        self.setMaximumWidth(400)
    
    # Adds the user guide widgets
    def add_userguide_widgets(self):
        # Adding the welcome label
        self.layout.addWidget(self.welcome_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Adding the info labels
        self.layout.addWidget(self.permission_image)
        self.layout.addWidget(self.permission_info_label)

        self.layout.addWidget(self.scan_image)
        self.layout.addWidget(self.scan_info_label)

        self.layout.addWidget(self.solve_image)
        self.layout.addWidget(self.solve_info_label)

        # Adding the start scanning button
        self.layout.addWidget(self.proceed_scan_button)
    
    # Starts the application
    def application_startup(self):
        self.add_userguide_widgets()

        self.setLayout(self.layout)
        self.setWindowTitle("CUBIX: User Guide")

    # Used to emit the proceed scan signal and allow the scan page to appear
    def start_scan_page(self):
        self.proceed_scan.emit()

