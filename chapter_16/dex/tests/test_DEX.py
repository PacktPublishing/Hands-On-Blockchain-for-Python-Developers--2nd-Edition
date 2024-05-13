import pytest


def test_addLiquidity(exchange, token, deployer):
    ETH = 100
    token.approve(exchange.address, 2000, sender=deployer)
    token_amount = 200
    exchange.addLiquidity(token_amount, value=ETH, sender=deployer)

    assert exchange.balance == ETH
    reserve = exchange.getReserve()
    assert reserve == token_amount


def test_getTokenAmount(exchange, token, deployer):
    token_amount = 20000
    token.approve(exchange.address, token_amount, sender=deployer)
    ETH = 10000
    exchange.addLiquidity(token_amount, value=ETH, sender=deployer)

    tokensOut = exchange.getTokenAmount(10)
    assert tokensOut == 19

    tokensOut = exchange.getTokenAmount(100)
    assert tokensOut == 198

    tokensOut = exchange.getTokenAmount(1000)
    assert tokensOut == 1818

    tokensOut = exchange.getTokenAmount(5000)
    assert tokensOut == 6666


def test_getETHAmount(exchange, token, deployer):
    token_amount = 20000
    token.approve(exchange.address, token_amount, sender=deployer)
    ETH = 10000
    exchange.addLiquidity(token_amount, value=ETH, sender=deployer)

    ethOut = exchange.getEthAmount(10)
    assert ethOut == 4

    ethOut = exchange.getEthAmount(100)
    assert ethOut == 49

    ethOut = exchange.getEthAmount(1000)
    assert ethOut == 476

    ethOut = exchange.getEthAmount(10000)
    assert ethOut == 3333

    ethOut = exchange.getEthAmount(15000)
    assert ethOut == 4285


def test_ethToTokenSwap(exchange, token, deployer, accounts):
    token_amount = 20000
    token.approve(exchange.address, token_amount, sender=deployer)
    ETH = 10000
    exchange.addLiquidity(token_amount, value=ETH, sender=deployer)

    exchange.ethToTokenSwap(15, value=10, sender=accounts[1])
    assert token.balanceOf(accounts[1]) == 19

    exchange.ethToTokenSwap(180, value=100, sender=accounts[2])
    assert token.balanceOf(accounts[2]) == 197

    exchange.ethToTokenSwap(1600, value=1000, sender=accounts[3])
    assert token.balanceOf(accounts[3]) == 1780


def test_tokenToEthSwap(exchange, token, deployer, accounts):
    token_amount = 20000
    token.approve(exchange.address, token_amount, sender=deployer)
    ETH = 10000
    exchange.addLiquidity(token_amount, value=ETH, sender=deployer)

    token.transfer(accounts[1], token_amount, sender=deployer)
    token.transfer(accounts[2], token_amount, sender=deployer)
    token.transfer(accounts[3], token_amount, sender=deployer)

    initial_balance = accounts[1].balance
    sold_token = 100
    ethAmount = 49
    token.approve(exchange.address, token_amount, sender=accounts[1])
    exchange.tokenToEthSwap(sold_token, 40, sender=accounts[1])
    assert token.balanceOf(accounts[1]) == token_amount - sold_token

    initial_balance = accounts[2].balance
    sold_token = 1000
    token.approve(exchange, sold_token, sender=accounts[2])
    exchange.tokenToEthSwap(sold_token, 400, sender=accounts[2])
    assert token.balanceOf(accounts[2]) == token_amount - sold_token
