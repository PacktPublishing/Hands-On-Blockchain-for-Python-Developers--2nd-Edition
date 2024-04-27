#pragma version ^0.3.0

event Lend:
    _borrower: indexed(address)
    _amount: indexed(uint256)

event Repay:
    _borrower: indexed(address)
    _amount: indexed(uint256)

interface ERC20_Interface:
    def transfer(_recipient: address, _amount: uint256): nonpayable
    def transferFrom(_sender: address, _recipient: address, _amount: uint256): nonpayable

token: public(address)
loan_amount: public(uint256)
collateral: public(uint256)
borrower: public(address)
loan_taken: public(bool)
interest: public(uint256)
owner: public(address)

@external
def __init__(_borrower: address,
             _token: address,
             _loan_amount: uint256,
             _collateral: uint256,
             _interest: uint256):
    self.token = _token
    self.loan_amount = _loan_amount
    self.collateral = _collateral
    self.borrower = _borrower
    self.interest = _interest
    self.owner = msg.sender

@external
@payable
def borrow():
    assert msg.sender == self.borrower, "Only the borrower can borrow the asset"
    assert msg.value == self.collateral, "Collateral is not enough"
    ERC20_Interface(self.token).transfer(msg.sender, self.loan_amount)
    self.loan_taken = True

    log Lend(msg.sender, self.loan_amount)

@external
def repay():
    assert msg.sender == self.borrower, "Only the borrower can repay the loan"
    assert self.loan_taken == True, "Loan has not been taken"

    cut: uint256 = self.interest * self.collateral / 100
    payback: uint256 = self.collateral - cut

    ERC20_Interface(self.token).transferFrom(msg.sender, self, self.loan_amount)
    send(msg.sender, payback)

    self.loan_taken = False

    log Repay(msg.sender, self.loan_amount)

@external
def withdraw_eth():
    assert msg.sender == self.owner, "Only the owner can withdraw ETH"
    assert self.loan_taken == False, "Cannot withdraw while loan is active"
    send(msg.sender, self.balance)
