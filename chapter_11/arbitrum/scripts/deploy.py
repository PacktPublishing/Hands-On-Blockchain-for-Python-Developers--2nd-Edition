from ape import accounts, project
import os


def main():
    password = os.environ["MY_PASSWORD"]
    dev = accounts.load("dev")
    dev.set_autosign(True, passphrase=password)
    contract = project.SimpleStorage.deploy(sender=dev)
    num_value = contract.retrieve.call()
    print(f"The num value is {num_value}")
