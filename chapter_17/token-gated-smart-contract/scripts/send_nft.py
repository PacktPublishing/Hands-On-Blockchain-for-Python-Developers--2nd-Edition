from ape import accounts, project
import os


def main():
    address = os.environ["NFT_ADDRESS"]
    destination = os.environ["NFT_RECIPIENT"]
    password = os.environ["MY_PASSWORD"]
    username = os.environ["ACCOUNT_USERNAME"]
    deployer = accounts.load(username)
    deployer.set_autosign(True, passphrase=password)
    contract = project.HelloNFT.at(address)
    contract.mint(destination, 1, sender=deployer)
