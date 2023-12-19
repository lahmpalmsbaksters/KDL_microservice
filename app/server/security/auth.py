import time
from typing import Dict
import jwt
from decouple import config
from server.database import (check_apikey)


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

expired_token_time = 60 * 60 * 24  # 24 hr timeout


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: dict) -> Dict[str, str]:
    payload = {
        "user_id": user["email"],
        "expires": time.time() + expired_token_time,
        "apikey": user["apikey"]
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def signupJWT(user: dict) -> Dict[str, str]:
    payload = {
        "user_id": user.email,
        "expires": time.time() + expired_token_time,
        "apikey": user.apikey
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


async def check_apikey_isvalid(user_apikey):
    result = await check_apikey(user_apikey)
    if result:
        return True  # API key is valid
    else:
        return False  # API key is not found in the database
