import os
import time
import jwt
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("HASHING_ALGORITHM")
JWT_ACCESS_LIFETIME = int(os.getenv("JWT_ACCESS_LIFETIME"))
JWT_REFRESH_LIFETIME = int(os.getenv("JWT_REFRESH_LIFETIME"))


def token_response(access_token: str, refresh_token: str, msg: str = None):
    return {"access": access_token, "refresh": refresh_token}


def signJWT(email: str) -> Dict[str, str]:
    access_payload = {"email": email, "expires": time.time() + JWT_ACCESS_LIFETIME * 60}
    refresh_payload = {
        "email": email,
        "expires": time.time() + JWT_REFRESH_LIFETIME * 24 * 60 * 60,
    }

    access_token = jwt.encode(
        payload=access_payload, key=SECRET_KEY, algorithm=ALGORITHM
    )
    refresh_token = jwt.encode(
        payload=refresh_payload, key=SECRET_KEY, algorithm=ALGORITHM
    )
    return token_response(access_token=access_token, refresh_token=refresh_token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
