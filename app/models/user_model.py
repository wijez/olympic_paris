from sqlalchemy import Column, UUID, String, Boolean, Enum

from app.core import Base
from app.utils import RoleEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
