from ape import accounts, project
import os


def main():
    password = os.environ["VOTER_PASSWORD"]
    address = os.environ["VOTING_APP_ADDRESS"]
    voter_account = os.environ["VOTER_ACCOUNT"]
    proposal = os.environ["PROPOSAL"]
    voter = accounts.load(voter_account)
    voter.set_autosign(True, passphrase=password)
    contract = project.VotingApp.at(address)
    contract.vote(proposal, sender=voter)
