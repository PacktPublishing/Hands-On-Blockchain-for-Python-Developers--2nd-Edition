from ape import accounts, project
import os


def main():
    password = os.environ["CHAIRPERSON_PASSWORD"]
    address = os.environ["VOTING_APP_ADDRESS"]
    voter_1 = os.environ["VOTER_1_ADDRESS"]
    voter_2 = os.environ["VOTER_2_ADDRESS"]
    voter_3 = os.environ["VOTER_3_ADDRESS"]
    chairperson = accounts.load("chairperson")
    chairperson.set_autosign(True, passphrase=password)
    contract = project.VotingApp.at(address)
    contract.giveRightToVote(voter_1, 1, sender=chairperson)
    contract.giveRightToVote(voter_2, 1, sender=chairperson)
    contract.giveRightToVote(voter_3, 1, sender=chairperson)
