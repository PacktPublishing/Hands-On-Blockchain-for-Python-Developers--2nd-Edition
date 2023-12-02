from ape import accounts, project
import os


def main():
    password = os.environ["VIDEO_ACCOUNT_PASSWORD"]
    deployer = accounts.load("video")
    deployer.set_autosign(True, passphrase=password)
    contract = project.VideoSharing.deploy(sender=deployer)
    print(f"The contract address is {contract.address}")
