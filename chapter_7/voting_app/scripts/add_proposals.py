from ape import accounts, project
import os


def main():
    password = os.environ["CHAIRPERSON_PASSWORD"]
    address = os.environ["VOTING_APP_ADDRESS"]
    chairperson = accounts.load("chairperson")
    chairperson.set_autosign(True, passphrase=password)
    contract = project.VotingApp.at(address)
    contract.addProposal("beach", sender=chairperson)
    contract.addProposal("mountain", sender=chairperson)
