import sys, os
from PySide6 import QtCore, QtWidgets
from ape import accounts


class TransferWidget(QtWidgets.QWidget):
    username = os.environ["WALLET_USERNAME"]
    password = os.environ["WALLET_PASSWORD"]

    def __init__(self):
        super().__init__()

        eth_label = QtWidgets.QLabel("ETH")
        self.amount_field = QtWidgets.QTextEdit("")
        self.amount_field.setFixedHeight(30)
        amount_layout = QtWidgets.QHBoxLayout()
        amount_layout.addWidget(self.amount_field)
        amount_layout.addWidget(eth_label)

        self.address_field = QtWidgets.QTextEdit("")
        self.address_field.setFixedHeight(30)
        self.address_field.setPlaceholderText("Address")
        self.transfer_button = QtWidgets.QPushButton("Transfer")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(amount_layout)
        self.layout.addWidget(self.address_field)
        self.layout.addWidget(self.transfer_button)

        self.transfer_button.clicked.connect(self.transfer_button_on_clicked)

    @QtCore.Slot()
    def transfer_button_on_clicked(self):
        address = self.address_field.toPlainText()
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
