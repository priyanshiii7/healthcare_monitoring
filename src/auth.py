from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# This handles password hashing
# bcrypt turns "mypassword123" into "$2b$12$xyz..." (unreadable)
# You can NEVER reverse it back — that's the point
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """Turns a plain password into a secure hash for storing in database."""
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain password matches the stored hash.
    Used during login.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expire_minutes:Optional[int] = None):
    """
    Creates a JWT token containing the user's info.
    
    The token encodes: who the user is + when it expires.
    Anyone with SECRET_KEY can verify it — but only your server has that key.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp":expire})

    # jwt.encode() creates the token string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token:str)-> Optional[dict]:
    """
    Decodes a JWT token and returns the data inside.
    Returns None if token is invalid or expired.
    """
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

