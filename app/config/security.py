from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from app.config.settings import settings
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)

def verify_pass(plain_pass: str, hashed_pass: str):
    return pwd_context.verify(plain_pass, hashed_pass)


def create_verification_token(user_id: int):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.VERIFICATION_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "type": "verify",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp())
    }

    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    return token

def decode_verification_token(token: str):
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    
    except JWTError:
        raise ValueError("Invaid token")
    
    if payload["type"] != "verify":
        raise ValueError("Invaid token")
    
    return payload


def create_access_token(user_id: int):

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": int(expire.timestamp())
    } 

    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str):

    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    except JWTError:
        raise ValueError("Invalid token")
    
    if payload["type"] != "access":
        raise ValueError("Invalid token")
    
    return payload