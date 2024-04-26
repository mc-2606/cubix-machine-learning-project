# Module imports
import sys
from PyQt6.QtWidgets import QApplication
from packages.scan_window import ScanWindow
from packages.solve_window import SolveWindow
from packages.user_guide import UserGuideWindow
from packages.modules.solve import solve_cube
from threading import Thread

# Central application
app = QApplication([])

# The scan and solve windows
scan_window = ScanWindow()
solve_window = SolveWindow()
user_guide_window = UserGuideWindow()

# Starts the initial scan process
def start_initial_scan_session():
    # Hiding the user guide window
    user_guide_window.hide()

    # Starting the application
    scan_window.application_startup()
    scan_window.show()

# Starts the scanning process
def start_scan_session():
    # Hiding the solve window
    solve_window.hide()

    # Showing the scan window
    scan_window.show()

# Starts a new solving session
def start_solve_session(scramble):
    # Hiding the scan window
    scan_window.hide()

    # Showing solve window
    solve_window.application_startup()
    solve_window.show()

    # Starting the solve
    solve_thread = Thread(target=solve_cube_async, args=(scramble, scan_window))
    solve_thread.start()


# Used to asynchronously run the a solve
def solve_cube_async(scramble, scan_window):
    # Predicting next moves
    predicted_moves = solve_cube(scramble)
   
    # Solutions text
    solutions_text = "Solutions: "

    # Adding move to the text label
    for count, move in enumerate(predicted_moves):
        solutions_text += str(move)
        solutions_text += "   "

        if count % 5 == 0:
            solutions_text += "\n"
   
    # Updating the solutions label
    solve_window.solutions_label.setText(solutions_text)


# Setting up function links
scan_window.scan_completed.connect(start_solve_session)
solve_window.new_solve.connect(start_scan_session)
user_guide_window.proceed_scan.connect(start_initial_scan_session)


# Main run window
def main():
    # Starting the user guide
    user_guide_window.application_startup()
    user_guide_window.show()

    # Executing application
    sys.exit(app.exec())