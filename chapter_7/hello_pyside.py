import sys
from PySide6 import QtCore, QtWidgets


class TextWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel("Hello Pyside")
        self.button = QtWidgets.QPushButton("Button")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = TextWidget()
    widget.show()

    sys.exit(app.exec())
