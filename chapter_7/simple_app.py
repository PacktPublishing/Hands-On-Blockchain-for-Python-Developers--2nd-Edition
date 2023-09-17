import sys
from PySide6 import QtCore, QtWidgets


class SimpleAppWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel("Hello")
        self.textedit = QtWidgets.QTextEdit("")
        self.button = QtWidgets.QPushButton("Say Hello")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textedit)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.button_on_clicked)

    @QtCore.Slot()
    def button_on_clicked(self):
        text = self.textedit.toPlainText()
        self.label.setText(f"Hello {text}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = SimpleAppWidget()
    widget.show()

    sys.exit(app.exec())
