# Module imports
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt


# Creating the solve window
class SolveWindow(QWidget):
    new_solve = pyqtSignal()

    def __init__(self):
        super(SolveWindow, self).__init__()

        # Creating the main layout
        self.layout = QVBoxLayout()

        # The solutions label
        self.solutions_label = QLabel()
        self.solutions_label.setText("Please wait, Solving the Rubiks Cube!!")
        self.solutions_label.setWordWrap(True)
        self.solutions_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # The new solve button
        self.new_solve_button = QPushButton()
        self.new_solve_button.setText("New Solve")
        self.new_solve_button.clicked.connect(self.start_new_solve)
        
        self.setFixedWidth(500)
    
    # Lets main program user wants to start a new solve
    def start_new_solve(self):
        self.new_solve.emit()
        self.solutions_label.setText("Please wait, Solving the Rubiks Cube!!")
        
    # Adds the solve widgets
    def add_solve_widgets(self):
        # Adding the solutions label
        self.layout.addWidget(self.solutions_label)
        self.layout.addWidget(self.new_solve_button)

    # Sets up the solve window
    def application_startup(self):
        # Adding all of the widgets
        self.add_solve_widgets()

        # Setting the title
        self.setLayout(self.layout)
        self.setWindowTitle("Solve")
    
