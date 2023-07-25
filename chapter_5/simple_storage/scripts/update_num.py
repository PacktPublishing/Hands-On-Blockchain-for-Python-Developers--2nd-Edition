from ape import accounts, project
import os


def main():
    password = os.environ["MY_PASSWORD"]
    address = os.environ["SIMPLE_STORAGE_ADDRESS"]
    dev = accounts.load("dev")
    dev.set_autosign(True, passphrase=password)
    contract = project.SimpleStorage.at(address)
    contract.store(19, sender=dev)
    print("Updating num value")
    num_value = contract.retrieve.call()
    print(f"The num value is {num_value}")
