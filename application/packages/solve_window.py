# Module imports
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from packages.modules.solve import solve_cube


# Creating the solve window
class SolveWindow(QWidget):
    def __init__(self):
        super(SolveWindow, self).__init__()

        # Creating the main layout
        self.layout = QVBoxLayout()

        # The solutions label
        self.solutions_label = QLabel()
        self.solutions_label.setText("Solutions: ")
    
    # Solving the Cube
    def solve_scramble(self, scramble):
        solve_cube(scramble)
        
    # Adds the solve widgets
    def add_solve_widgets(self):
        # Adding the solutions label
        self.layout.addWidget(self.solutions_label)

    # Sets up the solve window
    def application_startup(self):
        # Adding all of the widgets
        self.add_solve_widgets()

        # Setting the title
        self.setLayout(self.layout)
        self.setWindowTitle("Solve")
    
