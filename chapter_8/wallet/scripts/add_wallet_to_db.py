import sys, os, json
from PySide6 import QtCore, QtWidgets
from ape import accounts


class AddAddressToDbWidget(QtWidgets.QWidget):

    home_dir = os.path.expanduser('~')
    wallet_db_path = f"{home_dir}/.wallet.json"

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QFormLayout(self)
        self.save_button = QtWidgets.QPushButton("Save")
        self.address_field = QtWidgets.QTextEdit("")
        self.address_field.setFixedHeight(30)
        self.label_field = QtWidgets.QTextEdit("")
        self.label_field.setFixedHeight(30)
        self.layout.addRow("Address:", self.address_field)
        self.layout.addRow("Label:", self.label_field)
        self.layout.addRow("", self.save_button)

        self.save_button.clicked.connect(self.save_button_on_clicked)

    @QtCore.Slot()
    def save_button_on_clicked(self):
        address = self.address_field.toPlainText()
        label = self.label_field.toPlainText()
        if not os.path.exists(self.wallet_db_path):
            data = {}
        else:
            with open(self.wallet_db_path, "r") as f:
                data = json.load(f)
        data[label] = address
        with open(self.wallet_db_path, "w") as f:
            json.dump(data, f)
        self.close()


def main():
    app = QtWidgets.QApplication([])

    widget = AddAddressToDbWidget()
    widget.show()

    sys.exit(app.exec())
