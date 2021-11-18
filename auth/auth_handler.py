import jwt
from decouple import config

import time
from typing import Dict

from passlib.context import CryptContext

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def tokenresponse(token: str):
    return{
        "token_akses": token
    }

def signJWT(userID: str) -> Dict[str,str]:
    payload = {
        "userID" : userID,
        "masaberlaku" : time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return tokenresponse(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["masaberlaku"] >= time.time() else None
    except:
        return {}

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(original_password, hashed_password):
    return password_context.verify(original_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
        