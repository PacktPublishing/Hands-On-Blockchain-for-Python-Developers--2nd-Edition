# @version ^0.3.0

struct Voter:
    weight: uint256
    voted: bool
    delegate: address
    vote: uint256

struct Proposal:
    name: String[100]
    voteCount: uint256

voters: public(HashMap[address, Voter])
proposals: public(HashMap[uint256, Proposal])
voterCount: public(uint256)
chairperson: public(address)
amountProposals: public(uint256)

MAX_NUM_PROPOSALS: constant(uint256) = 3


@view
@internal
def _delegated(addr: address) -> bool:
    return self.voters[addr].delegate != empty(address)

@view
@external
def delegated(addr: address) -> bool:
    return self._delegated(addr)

@view
@internal
def _directlyVoted(addr: address) -> bool:
    return self.voters[addr].voted and (self.voters[addr].delegate == empty(address))

@view
@external
def directlyVoted(addr: address) -> bool:
    return self._directlyVoted(addr)

@external
def __init__():
    self.chairperson = msg.sender

@external
def addProposal(_proposalName: String[100]):
    assert msg.sender == self.chairperson
    i: uint256 = self.amountProposals
    self.proposals[i] = Proposal({
        name: _proposalName,
        voteCount: 0
    })
    self.amountProposals += 1

@external
def giveRightToVote(voter: address, _weight: uint256):
    assert msg.sender == self.chairperson
    assert not self.voters[voter].voted
    assert self.voters[voter].weight == 0
    self.voters[voter].weight = _weight
    self.voterCount += 1

@internal
def _forwardWeight(delegate_with_weight_to_forward: address):
    assert self._delegated(delegate_with_weight_to_forward)
    assert self.voters[delegate_with_weight_to_forward].weight > 0

    target: address = self.voters[delegate_with_weight_to_forward].delegate
    for i in range(4):
        if self._delegated(target):
            target = self.voters[target].delegate
        else:
            break

    weight_to_forward: uint256 = self.voters[delegate_with_weight_to_forward].weight
    self.voters[delegate_with_weight_to_forward].weight = 0
    self.voters[target].weight += weight_to_forward

    if self._directlyVoted(target):
        self.proposals[self.voters[target].vote].voteCount += weight_to_forward
        self.voters[target].weight = 0

@external
def delegate(to: address):
    assert not self.voters[msg.sender].voted
    assert to != msg.sender
    assert to != empty(address)

    self.voters[msg.sender].voted = True
    self.voters[msg.sender].delegate = to

    self._forwardWeight(msg.sender)

@external
def vote(proposal: uint256):
    assert not self.voters[msg.sender].voted
    assert proposal < self.amountProposals

    self.voters[msg.sender].vote = proposal
    self.voters[msg.sender].voted = True

    self.proposals[proposal].voteCount += self.voters[msg.sender].weight
    self.voters[msg.sender].weight = 0

@view
@internal
def _winningProposal() -> uint256:
    winning_vote_count: uint256 = 0
    winning_proposal: uint256 = 0
    for i in range(MAX_NUM_PROPOSALS):
        if self.proposals[i].voteCount > winning_vote_count:
            winning_vote_count = self.proposals[i].voteCount
            winning_proposal = i
    return winning_proposal

@view
@external
def winningProposal() -> uint256:
    return self._winningProposal()

@view
@external
def winnerName() -> String[100]:
    return self.proposals[self._winningProposal()].name
