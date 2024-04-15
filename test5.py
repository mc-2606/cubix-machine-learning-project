from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont

class CubeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors = [[QColor(0, 0, 0) for _ in range(3)] for _ in range(3)]  # Initialize with black color
        self.side_labels = ['Front', 'Right', 'Back', 'Left', 'Top', 'Bottom']

    def set_colors(self, colors):
        self.colors = colors
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Calculate the size of each cube section
        cube_size = min(width // 3, height // 3)

        for row in range(3):
            for col in range(3):
                # Calculate the position of the current cube section
                x = col * cube_size
                y = row * cube_size

                # Set the color for the current cube section
                color = self.colors[row][col]
                painter.setBrush(color)
                painter.drawRect(x, y, cube_size, cube_size)

        # Draw labels for each face
        font = QFont()
        font.setPixelSize(20)
        painter.setFont(font)

        for i, label in enumerate(self.side_labels):
            x = (i % 3) * cube_size
            y = (i // 3) * cube_size + cube_size // 2
            painter.drawText(x, y, label)
    
    def mousePressEvent(self, event):
        # Determine which cube section was clicked and update its color
        cube_size = min(self.width() // 3, self.height() // 3)
        row = event.pos().y() // cube_size
        col = event.pos().x() // cube_size

        # Toggle the color of the clicked cube section
        current_color = self.colors[row][col]
        new_color = QColor(255 - current_color.red(), 255 - current_color.green(), 255 - current_color.blue())
        self.colors[row][col] = new_color

        self.update()  # Trigger repaint after color change


import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cube Widget Example")

        self.cube_widget = CubeWidget()
        self.setCentralWidget(self.cube_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())