import uuid

from sqlalchemy import Column, UUID, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship

from app.core import Base
from app.utils import RoleEnum


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    verify_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    draft = relationship("Draft", back_populates="user")
