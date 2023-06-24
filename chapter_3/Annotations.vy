# @version ^0.3.0

author: String[100]
donatur: String[100]

@external
def __init__():
    self.author = "Arjuna Sky Kok"

@external
@pure
def add(x: int128, y: int128) -> int128:
    return x + y

@external
@view
def get_name_and_title() -> String[200]:
    return concat("Mr. ", self.author)

@external
@nonpayable
def change_name(new_name: String[100]):
    self.author = new_name

@external
@payable
def donate(donatur_name: String[100]):
    self.donatur = donatur_name
