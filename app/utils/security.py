from datetime import datetime, timedelta

import jwt
from jose import JWTError
from passlib.context import CryptContext

from app.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_reset_token(email: str):
    to_encode = {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        return email
    except JWTError:
        return None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    from app.crud import users_crud

    user = users_crud.get(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
