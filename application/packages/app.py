# Module imports
import sys
from PyQt6.QtWidgets import QApplication

# Application specific imports
from packages.scan_window import ScanWindow
from packages.solve_window import SolveWindow


# Main run function
def main():
    # Main application
    app = QApplication([])

    # Starts the solving process
    def start_solve(scramble):

        solve_window = SolveWindow()
        solve_window.solve_scramble(scramble)

        solve_window.application_startup()
        solve_window.show()
        

    # Adding scan window
    scan_window = ScanWindow()
    scan_window.application_startup()
    scan_window.show()

    # When a scan is completed, solving process begins
    scan_window.scan_compelted.connect(start_solve)

    sys.exit(app.exec())
