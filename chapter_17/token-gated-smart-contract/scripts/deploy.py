from ape import accounts, project
import os


def main():
    password = os.environ["MY_PASSWORD"]
    username = os.environ["ACCOUNT_USERNAME"]
    deployer = accounts.load(username)
    deployer.set_autosign(True, passphrase=password)
    contract = project.HelloNFT.deploy(sender=deployer)
    print(f"Deployed to {contract.address}")
