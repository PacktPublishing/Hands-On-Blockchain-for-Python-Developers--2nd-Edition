from siwe import SiweMessage
import siwe


eip_4361_string = """
service.org wants you to sign in with your Ethereum account:
0x8e6E9F42fB6d2052cf452A50B3550e1F7A04FaD0

I accept the ServiceOrg Terms of Service: https://service.org/tos

URI: https://service.org/login
Version: 1
Chain ID: 1
Nonce: 32891756
Issued At: 2021-09-30T16:25:24Z
Resources:
- ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq/
- https://example.com/my-web2-claim.json
"""
message = SiweMessage.from_message(message=eip_4361_string, abnf=False)
signature = "0xedb8936240893b956378822f3663d8a9c29f59ac904de206108768e5e054b4441cc673af036cef8bb90c0186017fa8db8f1551be97c176374c0a5bd2cacd27d91c"

try:
    message.verify(signature=signature)
    print("Signature is valid")
except siwe.VerificationError:
    print("Signature is invalid")
