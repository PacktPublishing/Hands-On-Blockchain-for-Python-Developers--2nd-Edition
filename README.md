# Hands-On Blockchain for Python Developers

<a href="https://www.packtpub.com/en-us/product/hands-on-blockchain-for-python-developers-9781805121367?utm_source=github&utm_medium=repository&utm_campaign="><img src="https://m.media-amazon.com/images/I/81VsvF1KTCL._SL1500_.jpg" alt="Hands-On Blockchain for Python Developers" height="256px" align="right"></a>

This is the code repository for [Hands-On Blockchain for Python Developers](https://www.packtpub.com/en-us/product/hands-on-blockchain-for-python-developers-9781805121367?utm_source=github&utm_medium=repository&utm_campaign=), published by Packt.

**Empowering Python developers in the world of blockchain and smart contracts**

## What is this book about?
We are living in the age of decentralized fi nance and NFTs. People swap tokens on Uniswap, borrow assets from Aave, send payments with stablecoins, trade art NFTs on OpenSea, and more. To build applications of this kind, you need to know how to write smart contracts.

This book covers the following exciting features:
* Understand blockchain and smart contracts
* Learn how to write smart contracts with Vyper
* Explore how to use the web3.py library and Ape Framework
* Discover related technologies such as Layer 2 and IPFS
* Gain a step-by-step guide to writing an automated market maker (AMM) decentralized exchange (DEX) smart contract
* Build innovative, interactive, and token-gated Web3 NFT applications

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1805121367) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders.

The code will look like the following:
```
from ape import accounts, project
import os
def main():
 password = os.environ["MY_PASSWORD"]
 dev = accounts.load("dev")
 dev.set_autosign(True, passphrase=password)
 contract = project.SimpleStorage.deploy(sender=dev)
 num_value = contract.retrieve.call()
 print(f"The num value is {num_value}")
```

**Following is what you need for this book:**
This blockchain book is for developers interested in understanding blockchain and smart contracts. It is suitable for both technology enthusiasts looking to explore blockchain technology and programmers who aspire to become smart contract engineers. Basic knowledge of GNU/Linux and Python programming is mandatory to get started with this book.

With the following software and hardware list you can run all code files present in the book (Chapter 1-17).
### Software and Hardware List
| Chapter | Software required | OS required |
| -------- | ------------------------------------ | ----------------------------------- |
| 1-17 | Python (minimum version 3.10 required) | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Vyper 0.3.10 (versions 0.4.x and above will not work) | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Ape Framework 0.7.23 (versions 0.8.x and above will not work) | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Modern browsers (Mozilla, Firefox, Chrome, etc) | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Remix | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Ganache | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Hardhat | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Geth | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Web3.py | Windows, Mac OS X, and Linux (Any) |
| 1-17 | PySide 6 | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Kubo | Windows, Mac OS X, and Linux (Any) |
| 1-17 | aioipfs | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Alchemy | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Infura | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Django | Windows, Mac OS X, and Linux (Any) |
| 1-17 | FastAPI | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Node.js | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Pnpm | Windows, Mac OS X, and Linux (Any) |
| 1-17 | React | Windows, Mac OS X, and Linux (Any) |
| 1-17 | Wagmi | Windows, Mac OS X, and Linux (Any) |
| 1-17 | MetaMask | Windows, Mac OS X, and Linux (Any) |

### Related products
* Solidity Programming Essentials [[Packt]](https://www.packtpub.com/en-ar/product/solidity-programming-essentials-9781803231181?utm_source=github&utm_medium=repository&utm_campaign=9781839216862) [[Amazon]](https://www.amazon.com/dp/1803231181)

* Applied Computational Thinking with Python [[Packt]](https://www.packtpub.com/en-IT/product/applied-computational-thinking-with-python-9781837632305?utm_source=github&utm_medium=repository&utm_campaign=9781803239545) [[Amazon]](https://www.amazon.com/dp/1837632308)

## Get to Know the Author
**Arjuna Sky Kok**
is a skilled software engineer with a passion for all things related to finance and
technology. He lives in Jakarta, where he studied mathematics and programming at Binus University.
Arjuna's academic achievements include double degrees in Computer Science and Mathematics.
Currently, he is focusing his talent in the crypto space, as he believes that DeFi and NFT will serve as
the foundation for future fi nance. He also has a keen interest in AI, especially Generative AI. Outside
of work, Arjuna enjoys watching anime, listening to J-pop songs, and playing basketball.
