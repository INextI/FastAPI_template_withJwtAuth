import bcrypt
from jwt import JWT
import jwt
from core.config import settings
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

def hashed_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)

def jwt_encode(payload: str, 
                private_key: str = settings.auth_jwt.private_key_path.read_text(), 
                algorihm: str = settings.auth_jwt.algorithm
                ) -> str:
    return JWT.encode(payload=payload, key=private_key, alg=algorihm)

def jwt_decode(token: str | bytes, 
               public_key: str = settings.auth_jwt.public_key_path.read_text(), 
               algorithm = settings.auth_jwt.algorithm
               ) -> dict[str, Any]:
    return JWT.decode(token, key=public_key, algorithms=[algorithm])

def create_access_token(data_in: dict, expire: timedelta | None = None) -> str:
    to_encode = data_in.copy()
    exp = datetime.now(timezone.utc) + (expire or timedelta(minutes=15))
    to_encode.update({'exp': exp})
    return jwt_encode(payload=to_encode)

def create_refresh_token(data_in: dict, expire: timedelta | None = None) -> str:
    to_encode = data_in.copy()
    exp = datetime.now(timezone.utc) + (expire or timedelta(days=30))
    to_encode.update({'exp': exp})
    return jwt_encode(payload=to_encode)

def decode_access_token(token: str | bytes) -> dict:
    try:
        return jwt_decode(token=token)
    except jwt.ExpiredSignatureError:
        raise Exception("Access token expire")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")

def decode_refresh_token(token: str | bytes) -> dict:
    try:
        return jwt_decode(token=token)
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token expire")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token")
