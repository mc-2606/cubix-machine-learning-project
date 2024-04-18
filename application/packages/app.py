
# Module imports
import sys
from PyQt6.QtWidgets import QApplication
from packages.scan_window import ScanWindow
from packages.solve_window import SolveWindow
from packages.modules.solve import solve_cube
from threading import Thread

# Central application
app = QApplication([])

# The scan and solve windows
scan_window = ScanWindow()
solve_window = SolveWindow()

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
    for move in predicted_moves:
        solutions_text += str(move)
        solutions_text += " "
    
    # Updating the solutions label
    solve_window.solutions_label.setText(solutions_text)


# Setting up function links
scan_window.scan_completed.connect(start_solve_session)
solve_window.new_solve.connect(start_scan_session)


# Main run window
def main():
    # Starting the application
    scan_window.application_startup()
    scan_window.show()

    # Executing application
    sys.exit(app.exec())



# # Function to start a new scan session
# def start_new_scan_session():
#     # Creating the scan window if it doesn'tks exist
#     scan_window = ScanWindow()

#     # The user has already accepted the camera feed, so we can just show the scan widgets
#     scan_window.application_startup()
#     scan_window.show()

#     # When a scan is completed, solving process begins
#     scan_window.scan_completed.connect(start_solve)

#     return scan_window

# # Function to start the solving process
# def start_solve(scramble):
#     # Creating the solve window
#     solve_window = SolveWindow()

#     # Showing the application
#     solve_window.application_startup()
#     solve_window.show()

#     # Start solving process in a separate thread
#     solve_thread = Thread(target=solve_cube_async, args=(scramble, solve_window))
#     solve_thread.start()

#     # When a new scan is requested, scanning process begins again
#     solve_window.new_solve.connect(start_new_scan_session)

#     return solve_window

# # Function to solve the cube asynchronously
# def solve_cube_async(scramble, solve_window:SolveWindow):
#     predicted_moves = solve_cube(scramble)
    
#     solutions_text = "Solutions: "

#     for move in predicted_moves:
#         solutions_text += str(move)
    
#     solve_window.solutions_label.setText(solutions_text)

# # Start the initial scan session
# sw = start_solve(['yellow', 'orange', 'green', 'white', 'white', 'orange', 'blue', 'blue', 'green', 'orange', 'green', 'orange', 'orange', 'red', 'red', 'white', 'white', 'yellow', 'yellow', 'yellow', 'red', 'green', 'green', 'green', 'white', 'red', 'yellow', 'white', 'blue', 'orange', 'yellow', 'orange', 'blue', 'green', 'red', 'blue', 'blue', 'red', 'red', 'white', 'blue', 'white', 'green', 'yellow', 'white', 'red', 'orange', 'orange', 'blue', 'yellow', 'yellow', 'red', 'green', 'blue'])

# # Execute the application
# app.exec()



    # # Creating the initial starting scan window
    # initial_scan_window = ScanWindow()
    # initial_scan_window.application_startup()
    # initial_scan_window.show()

    # # When a scan is completed, solving process begins
    # initial_scan_window.scan_compelted.connect(start_solve)

    # Executing application
    # sys.exit(app.exec())
