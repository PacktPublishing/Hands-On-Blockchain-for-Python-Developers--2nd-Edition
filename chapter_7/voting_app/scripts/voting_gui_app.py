from ape import accounts, project
import os, sys
from PySide6 import QtWidgets, QtCore


class VotingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel("Voting Blockchain App")

        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(["---"])

        self.button = QtWidgets.QPushButton("Vote")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.button_on_clicked)

    @QtCore.Slot()
    def button_on_clicked(self):
        proposal = self.combobox.currentText()
        index = self.combobox.currentIndex()
        print(f"The selected proposal is {proposal}")
        print(f"The selected index is {index}")


def main():
    voting_app_address = os.environ["VOTING_APP_ADDRESS"]
    contract = project.VotingApp.at(voting_app_address)
    amount_proposals = contract.amountProposals()

    app = QtWidgets.QApplication([])

    widget = VotingWidget()
    widget.show()

    for i in range(amount_proposals):
        proposal_name = contract.proposals(i).name
        widget.combobox.addItem(proposal_name)

    sys.exit(app.exec())
