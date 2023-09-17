from ape import accounts, project
import os


def main():
    password = os.environ["CHAIRPERSON_PASSWORD"]
    chairperson = accounts.load("chairperson")
    chairperson.set_autosign(True, passphrase=password)
    contract = project.VotingApp.deploy(sender=chairperson)
    chairperson = contract.chairperson()
    print(f"The chairperson account is {chairperson}")
