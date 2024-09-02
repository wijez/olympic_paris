from typing import Union

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr
