# Module imports
from cv2 import VideoCapture, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_DSHOW
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor

# Importing other important modules
from packages.modules.scan import convertimage_qt, generate_grid_positions, get_colours_from_grids, conv_colour_to_RGB, CORRESPONDING_SIDES


# Thread handler
class ImageThread(QThread):

    # Live Signal updates
    image_update = pyqtSignal(QImage)
    colour_update = pyqtSignal(list)

    # On thread.start()
    def run(self):
        self.thread_active = True

        # Capturing video + metadata
        capture = VideoCapture(0, CAP_DSHOW)
        width = capture.get(CAP_PROP_FRAME_WIDTH)
        height = capture.get(CAP_PROP_FRAME_HEIGHT)

        while self.thread_active:
            ret, frame = capture.read()

            # If camera is present
            if ret:
                # Image prep
                grid_positions = generate_grid_positions(width, height)

                # Fetching the colours
                colours = get_colours_from_grids(frame, grid_positions)
                converted_image = convertimage_qt(frame, grid_positions)  

                # Emitting the image
                self.image_update.emit(converted_image)
                
                # Emitting the colours at grid positions
                self.colour_update.emit(colours)

            # If no camera present
            else:
                raise Exception("[ERROR] Cannot locate camera video device")

    # To stop thread process
    def stop(self):
        self.thread_active = False
        self.quit()
    
class FaceWidget(QWidget):
    def __init__(self):
        super(FaceWidget, self).__init__()

        # Creating a white set of cubes
        self.colours = [[QColor(255, 255, 255) for _ in range(5)] for _ in range(5)]

    def paintEvent(self, event):
        # Creating a new painter to draw the boxes
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate the size of each cube section
        cube_size = min(self.width() // 5, self.height() // 5)

        # Creating the grid
        for row in range(5):
            for col in range(5):
                # Calculate the position of the current cube section
                x_pos = col * cube_size
                y_pos = row * cube_size

                # Drawing the main cube pieces correctly
                if row in range(1, 4) and col in range(1, 4):
                    # Set the colours for the current cube section
                    colour = self.colours[row][col]
                    painter.setBrush(colour)
                    painter.drawRoundedRect(x_pos, y_pos, cube_size, cube_size, 10, 10)

                # Drawing the correct edge pieces for the relative faces
                if not((row in [x for x in range(5) if x != 2] and col in [x for x in range(5) if x != 2]) or (row in range(1, 4) and col in range(1, 4))):
                    # Set the colours for the current cube section
                    colour = self.colours[row][col]
                    painter.setBrush(colour)
                    painter.drawRoundedRect(x_pos, y_pos, cube_size, cube_size, 50, 50)
    
    # Updates the relative sides of the faces
    def update_sides(self, current_colour):
        # Fetching the corresponding side colours
        top_colour = conv_colour_to_RGB(CORRESPONDING_SIDES[current_colour]['top'])
        bottom_colour = conv_colour_to_RGB(CORRESPONDING_SIDES[current_colour]['bottom'])
        left_colour = conv_colour_to_RGB(CORRESPONDING_SIDES[current_colour]['left'])
        right_colour = conv_colour_to_RGB(CORRESPONDING_SIDES[current_colour]['right'])
        assignment_order = [top_colour, left_colour, right_colour, bottom_colour]

        # Keeping track of which colour to update
        count = 0

        # Adjusting the colours of the edges
        for row in range(5):
            for col in range(5):

                # If on the correct edges
                if not((row in [x for x in range(5) if x != 2] and col in [x for x in range(5) if x != 2]) or (row in range(1, 4) and col in range(1, 4))):

                    # Assigns the new colour pieces
                    colour = assignment_order[count]
                    self.colours[row][col] = QColor(colour[0], colour[1], colour[2])

                    # Updating the assignment order
                    count += 1


    # Updates the colours of each cube piece
    def update_colours(self, colours, current_colour):
        # Converting colours to RGB tuples
        colours = [conv_colour_to_RGB(colour) for colour in colours]

        # Rearranging colours as they are scanned differently
        updated_colours = [
            [colours[0], colours[3], colours[6]],
            [colours[1], colours[4], colours[7]],
            [colours[2], colours[5], colours[8]]
        ]

        # Iterating over the colours
        for row in range(len(updated_colours)):
            for column in range(len(updated_colours[row])):
                fetched_colour = updated_colours[row][column]

                # If centrepiece
                if row == 1 and column == 1:
                    # Permanently assigns the colour so they know what side they are scanning
                    rgb_val = conv_colour_to_RGB(current_colour)
                    self.colours[row + 1][column + 1] = QColor(rgb_val[0], rgb_val[1], rgb_val[2])

                else:
                    # Getting the RGB values
                    red_val = fetched_colour[0]
                    green_val = fetched_colour[1]
                    blue_val = fetched_colour[2]

                    # Setting the colours to the new RGB value
                    self.colours[row + 1][column + 1] = QColor(red_val, green_val, blue_val)
                
                # Updating the next sides
                self.update_sides(current_colour)

        # Used to fully update the values
        self.update()

# The scan window
class ScanWindow(QWidget):
    # When the scan is completed
    scan_compelted = pyqtSignal(list)

    # OOP inheritance from QWidget
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

        # Tracking the colours scanned
        self.cube_side_colours = []
        self.current_grid_colours = []

        # Creating main layout
        self.layout = QVBoxLayout()

        # Adding main widgets
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

        # Scan button
        self.scan_button = QPushButton()
        self.scan_button.setText("Scan Side")
        self.scan_button.clicked.connect(self.increment_scan)

        # Which side to currently scan + scanned sides
        self.current_scan = 0
        self.current_side = QLabel()
        self.current_side.setText("Scan: " + self.SCAN_ORDER[self.current_scan])
        
        self.scanned = "Scanned sides: "
        self.scanned_sides = QLabel()
        self.scanned_sides.setText(self.scanned)

        # New Scan button
        self.new_scan_button = QPushButton()
        self.new_scan_button.setText("New Scan")
        self.new_scan_button.clicked.connect(self.start_new_scan)
        
        # Updating grid colours
        self.image_thread = ImageThread()
        self.image_thread.colour_update.connect(self.process_grid_colours)

        # Creating the face widget
        self.face_widget = FaceWidget()
        self.face_widget.setFixedSize(200, 200)
        self.setFixedWidth(500)

    # Verifies that the cube has been scanned properly
    def verify_valid_scan(self):
        count_colours = {}

        # Keeping track of the colours and how many times they appear
        for colour in self.cube_side_colours:
            count_colours[colour] = count_colours.get(colour, 0 ) + 1

            # If any of the colours exceed 9
            if count_colours[colour] > 9:
                return False

        # The colours are correct
        return True


    # Updates the scanned sides
    def increment_scan(self):
        # Whilst the scans are less than 6 (comparing the index)
        if self.current_scan < 6:
            # Updating variables
            side = self.SCAN_ORDER[self.current_scan]
            self.scanned += (side + ", ")

            # Updating widget text
            if self.current_scan == 5:
                self.current_side.setText("Scan Completed")
            else:
                self.current_side.setText(f"Scan: {self.SCAN_ORDER[self.current_scan+1]}")
            
            # Updating scanned sides
            self.scanned_sides.setText(self.scanned)

            # Incrementing scan
            self.current_scan += 1

            # Adding the grid colours of the scan to the cube
            self.cube_side_colours += self.current_grid_colours

            # When the final scan
            if self.current_scan == 6:
                
                # Verifying if solve is valid
                if self.verify_valid_scan():
                    # Stops the image thread for performance
                    self.image_thread.stop()

                    # Lets main program know that the scanning process has been finished
                    self.scan_compelted.emit(self.cube_side_colours)
                    self.hide()
                
                # If the solve is not valid
                else:
                    # Creating a message so that they have scanned the cube incorrectly
                    message = QMessageBox()
                    message.setText("Error")
                    message.setInformativeText("Please make sure you scan each side properly!")

                    message.exec()

                    # Starts a new scan
                    self.start_new_scan()
        
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
        # Adding scan instructions
        self.layout.addWidget(self.current_side)
        self.layout.addWidget(self.scanned_sides)

        # Addin scan info
        self.layout.addWidget(self.view_finder)
        self.layout.addWidget(self.face_widget)

        # Adding scan buttons
        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.new_scan_button)
    
    
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

    # Updates the class colour state
    def process_grid_colours(self, grid_colours):
        if self.current_scan == 6:
            return
        else:
            # setting the current grid colours
            self.current_grid_colours = grid_colours

            # Updating the colours of the face widget
            self.face_widget.update_colours(self.current_grid_colours, self.SCAN_ORDER[self.current_scan].lower())
    
    # To start a new scan
    def start_new_scan(self):
        # Resetting the side colours
        self.cube_side_colours = []

        # Setting current scan to 0
        self.current_scan = 0
        self.current_side.setText("Scan: " + self.SCAN_ORDER[self.current_scan])
        
        # Resetting the scanned sides
        self.scanned = "Scanned sides: "
        self.scanned_sides.setText(self.scanned)
    
