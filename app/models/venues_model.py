from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core import Base


class Venues(Base):
    __tablename__ = "venues"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    url = Column(String)

    events = relationship("Events", back_populates="venue")


