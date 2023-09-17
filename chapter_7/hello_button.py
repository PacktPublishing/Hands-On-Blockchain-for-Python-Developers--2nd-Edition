import sys
from PySide6 import QtCore, QtWidgets


class ButtonWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Button")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.button_on_clicked)

    @QtCore.Slot()
    def button_on_clicked(self):
        print("Clicking the button")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ButtonWidget()
    widget.show()

    sys.exit(app.exec())
