from ape import accounts, project
import os


def main():
    address = os.environ["VIDEO_SHARING_ADDRESS"]
    password = os.environ["VIDEO_ACCOUNT_PASSWORD"]
    destination = os.environ["DESTINATION_ADDRESS"]
    account = os.environ["VIDEO_ACCOUNT"]
    deployer = accounts.load(account)
    deployer.set_autosign(True, passphrase=password)
    contract = project.VideoSharing.at(address)
    contract.transfer(destination, 100, sender=deployer)
