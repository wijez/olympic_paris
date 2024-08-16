from passlib.context import CryptContext

from app.crud import users_crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = users_crud.get(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
