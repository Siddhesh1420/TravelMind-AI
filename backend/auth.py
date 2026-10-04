import os
import json
import hashlib
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

USERS_FILE = "users.json"
MCP_TOKEN = os.getenv("MCP_SECRET_TOKEN", "mcp-internal-token")

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Load users from file on startup
users_db = load_users()


def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password[:72].encode(),
        salt,
        100000
    )
    return salt.hex() + ':' + key.hex()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        salt_hex, key_hex = hashed.split(':')
        salt = bytes.fromhex(salt_hex)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain[:72].encode(),
            salt,
            100000
        )
        return key.hex() == key_hex
    except:
        return False

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    if token == MCP_TOKEN:
        return "mcp_user"
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")