from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], depreated="auto")

def hash_pass(password: str) -> str:
    return pwd_context.hash(password)