from datetime import datetime, timedelta, timezone
from string import Template
import string
import json
import secrets
import os
from typing import Union

from ape import Contract
from ape import networks
from ethpm_types import ContractType

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel
from typing_extensions import Annotated
from siwe import SiweMessage
import siwe

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

EIP_4361_STRING = Template("""
packtpub.com wants you to sign in with your Ethereum account:
$address

I accept the PacktPub Terms of Service: https://www.packtpub.com/en-us/help/terms-and-conditions

URI: http://127.0.0.1:8000/token
Version: 1
Chain ID: 1
Nonce: $nonce
Issued At: $nonce_time
Resources:
- https://github.com/PacktPublishing/Hands-On-Blockchain-for-Python-Developers--2nd-Edition
""")

nonces_data = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str
 
class Nonce(BaseModel):
    nonce: str
    nonce_time: str

class Crypto(BaseModel):
    address: str
    signature: str

class User(BaseModel):
    address: str

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_nonce(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/nonce/{address}")
async def nonce(address: str) -> Nonce:
    nonce = generate_nonce()
    nonce_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    nonces_data[address] = {"nonce": nonce, "nonce_time": nonce_time}
    return nonces_data[address]

@app.post("/token")
async def login_for_access_token(
  crypto: Crypto,
) -> Token:
    address = crypto.address
    nonce = nonces_data[address]["nonce"]
    nonce_time = nonces_data[address]["nonce_time"]
    signature = crypto.signature
    eip_string = EIP_4361_STRING.substitute(address=address, nonce=nonce, nonce_time=nonce_time)
    message = SiweMessage.from_message(message=eip_string, abnf=False)
    try:
        message.verify(signature=signature)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": address}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    except siwe.VerificationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect signature",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        address: str = payload.get("sub")
        if address is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    exists = address in nonces_data
    if not exists:
        raise credentials_exception
    return User(address=address)

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@app.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

BLOCKCHAIN_NETWORK = "local"
BLOCKCHAIN_PROVIDER = "geth"

@app.get("/content")
async def read_content(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    with open('../token-gated-smart-contract/.build/HelloNFT.json') as f:
        contract = json.load(f)
        abi = contract['abi']

    nft_address = os.environ["NFT_ADDRESS"]
    with networks.ethereum[BLOCKCHAIN_NETWORK].use_provider(BLOCKCHAIN_PROVIDER):
        ct = ContractType.parse_obj({"abi": abi})
        NFTSmartContract = Contract(nft_address, ct)
        own_nft = NFTSmartContract.balanceOf(current_user.address) > 0

    if own_nft:
        return {"content": "Premium content"}
    else:
        return {"content": "Basic content"}
