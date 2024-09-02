import uuid

from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func
import enum

from app.core import Base
from app.utils import DraftStatus


class Draft(Base):
    __tablename__ = 'drafts'

    id = Column(UUID(as_uuid=True), primary_key=True,  default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    status = Column(Enum(DraftStatus), default=DraftStatus.draft)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="draft")
