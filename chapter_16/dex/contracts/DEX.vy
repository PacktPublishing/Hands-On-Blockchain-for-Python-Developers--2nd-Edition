# @version ^0.3.0
# @dev Implementation of Uniswap V1 part 1.
# @author Arjuna Sky Kok (@arjunaskykok)
# Based on https://jeiwan.net/posts/programming-defi-uniswap-1/


from vyper.interfaces import ERC20 as IERC20


interface Exchange:
    def getReserve() -> uint256: view
    def getAmount(inputAmount: uint256,
                  inputReserve: uint256,
                  outputReserve: uint256) -> uint256: view

tokenAddress: public(address)


@external
def __init__(_token: address):
    assert _token != ZERO_ADDRESS, "invalid token address"

    self.tokenAddress = _token


@external
@payable
def addLiquidity(_tokenAmount: uint256):
    token: IERC20 = IERC20(self.tokenAddress)
    token.transferFrom(msg.sender, self, _tokenAmount)


@external
@view
def getReserve() -> uint256:
    return IERC20(self.tokenAddress).balanceOf(self)


@external
@view
def getAmount(inputAmount: uint256,
              inputReserve: uint256,
              outputReserve: uint256) -> uint256:
    assert inputReserve > 0 and outputReserve > 0, "invalid reserves"

    return (inputAmount * outputReserve) / (inputReserve + inputAmount)


@external
@view
def getTokenAmount(_ethSold: uint256) -> uint256:
    assert _ethSold > 0, "ethSold is too small"

    tokenReserve : uint256 = Exchange(self).getReserve()

    return Exchange(self).getAmount(_ethSold, self.balance, tokenReserve)


@external
@view
def getEthAmount(_tokenSold: uint256) -> uint256:
    assert _tokenSold > 0, "tokenSold is too small"

    tokenReserve : uint256 = Exchange(self).getReserve()

    return Exchange(self).getAmount(_tokenSold, tokenReserve, self.balance)


@external
@payable
def ethToTokenSwap(_minTokens: uint256):
    tokenReserve : uint256 = Exchange(self).getReserve()
    tokensBought : uint256 = Exchange(self).getAmount(msg.value,
                                       self.balance - msg.value,
                                       tokenReserve)

    assert tokensBought >= _minTokens, "insufficient output amount"

    IERC20(self.tokenAddress).transfer(msg.sender, tokensBought)


@external
def tokenToEthSwap(_tokensSold: uint256, _minEth: uint256):
    tokenReserve: uint256 = Exchange(self).getReserve()
    ethBought: uint256 = Exchange(self).getAmount(_tokensSold,
                                   tokenReserve,
                                   self.balance)

    assert ethBought >= _minEth, "insufficient output amount"

    IERC20(self.tokenAddress).transferFrom(msg.sender, self, _tokensSold)
    send(msg.sender, ethBought)
