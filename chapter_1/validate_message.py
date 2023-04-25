from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def fetch_public_key(user):
    with open(user.decode('ascii') + "key.pub", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
           key_file.read(),
           backend=default_backend())
    return public_key

# Message coming from user
message = b"Nelson likes cat"

# Signature coming from user
signature = b'\x98\xe3\xd0\xae\xbb7\x1e\x04?AP\x98\xd9\x9cs\x12\x13\x14\xe9\x03\xaa\x94\xc8\xd7\xea;\xc9\xc5\xb5~\xa8c\xe2\n\xeb\x97\xe6\xcb\x8f$\x1a\x82\xd7n4tf\xbe\xd4\xb8\xd1^L\xd0\x98J\x9d\x93\xb9$\xe1e\x87\xaa\xadV\xd0%\xa3\xa7\xb5R/\x15\x17\xd6 \xe3\x91\xa9\x1c\x90\xef\x8eNS\xa6\x92\x9f\xb4B\x8dv\xbfs{\xd2\xf6m\t\x93)\x10U\x04\xe0\x81\x97\x80T\x94\xcb\x0f\x18\xbd\x0f\xb3\xbe"\xf8\xb8U\xc5\xf7\xfb^\xd5@'

user = message.split()[0].lower()
# fetch public key from Nelson
public_key = fetch_public_key(user)
# … verify the message like before
public_key.verify(
    signature,
    message,
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256())
