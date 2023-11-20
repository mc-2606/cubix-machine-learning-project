# Module imports
from PyQt6.QtWidgets import QApplication

# Application specific imports
from packages.scan_window import ScanWindow

# Main application
app = QApplication([])

# Adding scan window
scan_window = ScanWindow()
scan_window.start_viewfinder_thread()
scan_window.show()