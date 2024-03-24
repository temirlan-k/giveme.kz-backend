
import os
import time
from typing import Dict
import jwt
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('HASHING_ALGORITHM')
JWT_ACCESS_LIFETIME=config('JWT_ACCESS_LIFETIME',cast=int) # minutes
JWT_REFRESH_LIFETIME=config('JWT_REFRESH_LIFETIME',cast=int) # days



def token_response(access_token:str,refresh_token:str,msg:str=None):
    return {
        "access":access_token,
        "refresh":refresh_token
    }

def signJWT(email:str)-> Dict[str,str]:
    access_payload={
        'email':email,
        'expires':time.time() + JWT_ACCESS_LIFETIME * 60
    }
    refresh_payload={
        'email':email,
        'expires':time.time()+ JWT_REFRESH_LIFETIME * 24 * 60 * 60
    }
    
    access_token=jwt.encode(payload=access_payload,key=SECRET_KEY,algorithm=ALGORITHM)
    refresh_token=jwt.encode(payload=refresh_payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token_response(access_token=access_token,refresh_token=refresh_token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}  