import sys, os, json
from PySide6 import QtCore, QtWidgets
from ape import accounts


class TransferWidget(QtWidgets.QWidget):
    username = os.environ["WALLET_USERNAME"]
    password = os.environ["WALLET_PASSWORD"]
    home_dir = os.path.expanduser('~')
    wallet_db_path = f"{home_dir}/.wallet.json"

    def __init__(self):
        super().__init__()

        eth_label = QtWidgets.QLabel("ETH")
        self.amount_field = QtWidgets.QTextEdit("")
        self.amount_field.setFixedHeight(30)
        amount_layout = QtWidgets.QHBoxLayout()
        amount_layout.addWidget(self.amount_field)
        amount_layout.addWidget(eth_label)

        self.address_combobox = QtWidgets.QComboBox()
        if not os.path.exists(self.wallet_db_path):
            data = {}
        else:
            with open(self.wallet_db_path, "r") as f:
                data = json.load(f)
        options = ["---"]
        for k,v in data.items():
            options.append(k + " - " + v)
        self.address_combobox.addItems(options)

        self.transfer_button = QtWidgets.QPushButton("Transfer")
        self.transfer_button.clicked.connect(self.transfer_button_on_clicked)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(amount_layout)
        self.layout.addWidget(self.address_combobox)
        self.layout.addWidget(self.transfer_button)

    @QtCore.Slot()
    def transfer_button_on_clicked(self):
        label_address = self.address_combobox.currentText()
        if label_address == "---":
            return
        label, address = label_address.split(" - ")
        amount = self.amount_field.toPlainText()
        amount = amount + "000000000000000000"
        wallet_account = accounts.load(self.username)
        wallet_account.set_autosign(True, passphrase=self.password)
        wallet_account.transfer(address, amount)
        self.close()


def main():
    app = QtWidgets.QApplication([])

    widget = TransferWidget()
    widget.show()

    sys.exit(app.exec())
