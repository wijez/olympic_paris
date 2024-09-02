from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.orm import relationship

from app.core import Base


class Venues(Base):
    __tablename__ = "venues"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    url = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    events = relationship("Events", back_populates="venue")


