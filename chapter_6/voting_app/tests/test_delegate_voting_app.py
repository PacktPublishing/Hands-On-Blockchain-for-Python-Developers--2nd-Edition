import pytest
from ape.exceptions import ContractLogicError

def test_delegate(delegate_contract, deployer, accounts):
    user = accounts[1]
    user2 = accounts[2]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)

    assert delegate_contract.voters(user).weight == 1
    assert delegate_contract.voters(user).voted == False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 2
    assert delegate_contract.voters(user2).voted == False
    assert delegate_contract.voters(user2).vote == 0
    delegate_contract.delegate(user, sender=user2)
    assert delegate_contract.voters(user).weight == 3
    assert delegate_contract.voters(user).voted == False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 0
    assert delegate_contract.voters(user2).voted == True
    assert delegate_contract.voters(user2).vote == 0

def test_delegate_2_levels(delegate_contract, deployer, accounts):
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)
    delegate_contract.giveRightToVote(user3, 5, sender=deployer)

    assert delegate_contract.voters(user).weight == 1
    assert delegate_contract.voters(user).voted == False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 2
    assert delegate_contract.voters(user2).voted == False
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user3).weight == 5
    assert delegate_contract.voters(user3).voted == False
    assert delegate_contract.voters(user3).vote == 0
    delegate_contract.delegate(user, sender=user2)
    delegate_contract.delegate(user2, sender=user3)
    assert delegate_contract.voters(user).weight == 8
    assert delegate_contract.voters(user).voted == False
    assert delegate_contract.voters(user).vote == 0
    assert delegate_contract.voters(user2).weight == 0
    assert delegate_contract.voters(user2).voted == True
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user3).weight == 0
    assert delegate_contract.voters(user3).voted == True
    assert delegate_contract.voters(user3).vote == 0

def test_vote_after_delegate_2_levels(delegate_contract, deployer, accounts):
    delegate_contract.addProposal("beach", sender=deployer)
    delegate_contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)
    delegate_contract.giveRightToVote(user3, 5, sender=deployer)
    delegate_contract.delegate(user, sender=user2)
    delegate_contract.delegate(user2, sender=user3)
    delegate_contract.vote(1, sender=user)
    assert delegate_contract.voters(user).weight == 0
    assert delegate_contract.voters(user).voted == True
    assert delegate_contract.voters(user).vote == 1
    assert delegate_contract.winnerName() == "mountain"
    assert delegate_contract.proposals(0).voteCount == 0
    assert delegate_contract.proposals(1).voteCount == 8

def test_delegate_after_vote(delegate_contract, deployer, accounts):
    delegate_contract.addProposal("beach", sender=deployer)
    delegate_contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    delegate_contract.giveRightToVote(user, 1, sender=deployer)
    delegate_contract.giveRightToVote(user2, 2, sender=deployer)
    delegate_contract.giveRightToVote(user3, 5, sender=deployer)
    delegate_contract.vote(1, sender=user)
    delegate_contract.delegate(user, sender=user2)
    delegate_contract.delegate(user2, sender=user3)

    assert delegate_contract.voters(user2).weight == 0
    assert delegate_contract.voters(user2).voted == True
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user2).delegate == user
    assert delegate_contract.voters(user3).weight == 0
    assert delegate_contract.voters(user3).voted == True
    assert delegate_contract.voters(user2).vote == 0
    assert delegate_contract.voters(user3).delegate == user2

    assert delegate_contract.voters(user).weight == 0
    assert delegate_contract.voters(user).voted == True
    assert delegate_contract.voters(user).vote == 1
    assert delegate_contract.voters(user).delegate == "0x0000000000000000000000000000000000000000"

    assert delegate_contract.winnerName() == "mountain"
    assert delegate_contract.proposals(0).voteCount == 0
    assert delegate_contract.proposals(1).voteCount == 8

def test_chairperson(delegate_contract, deployer):
    contract = delegate_contract
    chairperson = contract.chairperson()
    assert chairperson == deployer

def test_addProposal(delegate_contract, deployer):
    contract = delegate_contract
    assert contract.amountProposals() == 0
    assert contract.proposals(0).name == ""
    contract.addProposal("beach", sender=deployer)
    assert contract.amountProposals() == 1
    assert contract.proposals(0).name == "beach"

def test_addProposal_fail(delegate_contract, accounts):
    contract = delegate_contract
    with pytest.raises(ContractLogicError):
        contract.addProposal("beach", sender=accounts[1])

def test_giveRightToVote(delegate_contract, deployer, accounts):
    contract = delegate_contract
    user = accounts[1]
    assert contract.voterCount() == 0
    assert contract.voters(user).weight == 0
    contract.giveRightToVote(user, 1, sender=deployer)
    assert contract.voterCount() == 1
    assert contract.voters(user).weight == 1

    power_user = accounts[2]
    assert contract.voters(power_user).weight == 0
    contract.giveRightToVote(power_user, 9, sender=deployer)
    assert contract.voterCount() == 2
    assert contract.voters(power_user).weight == 9

def test_giveRightToVote_fail(delegate_contract, deployer, accounts):
    contract = delegate_contract
    user = accounts[1]
    with pytest.raises(ContractLogicError):
        contract.giveRightToVote(user, 1, sender=accounts[1])

def test_vote(delegate_contract, deployer, accounts):
    contract = delegate_contract
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    user2 = accounts[2]
    contract.giveRightToVote(user, 1, sender=deployer)
    contract.giveRightToVote(user2, 1, sender=deployer)

    assert contract.voters(user).weight == 1
    assert contract.voters(user).voted == False
    assert contract.voters(user).vote == 0
    assert contract.proposals(0).voteCount == 0
    contract.vote(0, sender=user)
    assert contract.proposals(0).voteCount == 1
    assert contract.voters(user).weight == 0
    assert contract.voters(user).voted == True
    assert contract.voters(user).vote == 0

    assert contract.voters(user2).weight == 1
    assert contract.voters(user2).voted == False
    assert contract.voters(user2).vote == 0
    assert contract.proposals(1).voteCount == 0
    contract.vote(1, sender=user2)
    assert contract.proposals(1).voteCount == 1
    assert contract.voters(user2).weight == 0
    assert contract.voters(user2).voted == True
    assert contract.voters(user2).vote == 1

def test_vote_fail(delegate_contract, deployer, accounts):
    contract = delegate_contract
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user = accounts[1]
    contract.giveRightToVote(user, 1, sender=deployer)

    contract.vote(0, sender=user)
    with pytest.raises(ContractLogicError):
        contract.vote(0, sender=user)

def test_winnerName(delegate_contract, deployer, accounts):
    contract = delegate_contract
    contract.addProposal("beach", sender=deployer)
    contract.addProposal("mountain", sender=deployer)
    user1 = accounts[1]
    user2 = accounts[2]
    user3 = accounts[3]
    contract.giveRightToVote(user1, 1, sender=deployer)
    contract.giveRightToVote(user2, 1, sender=deployer)
    contract.giveRightToVote(user3, 1, sender=deployer)

    contract.vote(0, sender=user1)
    contract.vote(1, sender=user2)
    contract.vote(1, sender=user3)

    assert contract.proposals(0).voteCount == 1
    assert contract.proposals(1).voteCount == 2
    assert contract.winnerName() == "mountain"
