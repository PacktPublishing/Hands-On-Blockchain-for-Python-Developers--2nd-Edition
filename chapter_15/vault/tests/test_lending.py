def test_init(lending_contract, deployer, give_token, borrower):
    assert borrower == lending_contract.borrower()

def test_borrow(lending_contract, token_contract, deployer, give_token, borrower):
    collateral = 1 * 10 ** 18
    approved_amount = 10000
    loan_amount = 1000
    assert lending_contract.loan_taken() == False
    assert token_contract.balanceOf(borrower) == 0
    assert lending_contract.balance == 0
    lending_contract.borrow(value=collateral, sender=borrower)
    assert lending_contract.loan_taken() == True
    assert token_contract.balanceOf(borrower) == loan_amount
    assert lending_contract.balance == collateral

def test_repay(lending_contract, token_contract, deployer, give_token, borrower):
    collateral = 1 * 10 ** 18
    approved_amount = 10000
    loan_amount = 1000
    lending_contract.borrow(value=collateral, sender=borrower)
    interest = collateral / 10

    token_contract.approve(lending_contract, approved_amount, sender=borrower)
    assert lending_contract.loan_taken() == True
    assert token_contract.balanceOf(borrower) == loan_amount
    assert lending_contract.balance == collateral
    lending_contract.repay(sender=borrower)
    assert lending_contract.loan_taken() == False
    assert token_contract.balanceOf(borrower) == 0
    assert lending_contract.balance == interest
