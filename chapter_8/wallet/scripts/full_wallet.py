import sys, os, json, time
from PySide6 import QtCore, QtWidgets
from ape import accounts


class WorkerThread(QtCore.QThread):
    username = os.environ["WALLET_USERNAME"]
    update_label = QtCore.Signal(str)

    def run(self):
        while True:
            time.sleep(1)
            wallet_account = accounts.load(self.username)
            self.update_label.emit(str(wallet_account.balance))


class TransferWidget(QtWidgets.QWidget):
    username = os.environ["WALLET_USERNAME"]
    password = os.environ["WALLET_PASSWORD"]
    home_dir = os.path.expanduser('~')
    wallet_db_path = f"{home_dir}/.wallet.json"

    def __init__(self):
        super().__init__()

        balance_layout = QtWidgets.QHBoxLayout()
        balance_label = QtWidgets.QLabel("My Balance:")
        self.balance_field = QtWidgets.QLabel("ETH")
        balance_layout.addWidget(balance_label)
        balance_layout.addWidget(self.balance_field)

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
        self.layout.addLayout(balance_layout)
        self.layout.addLayout(amount_layout)
        self.layout.addWidget(self.address_combobox)
        self.layout.addWidget(self.transfer_button)

        self.wallet_account = accounts.load(self.username)
        self.wallet_account.set_autosign(True, passphrase=self.password)

        self.thread = WorkerThread()
        self.thread.update_label.connect(self.update_balance)
        self.thread.start()

    def update_balance(self, balance):
        balance = int(balance) / 10**18
        self.balance_field.setText(str(balance) + " ETH")

    @QtCore.Slot()
    def transfer_button_on_clicked(self):
        label_address = self.address_combobox.currentText()
        if label_address == "---":
            return
        label, address = label_address.split(" - ")
        amount = self.amount_field.toPlainText()
        amount = amount + "000000000000000000"
        self.wallet_account.transfer(address, amount)
        self.close()


def main():
    app = QtWidgets.QApplication([])

    widget = TransferWidget()
    widget.show()

    sys.exit(app.exec())
