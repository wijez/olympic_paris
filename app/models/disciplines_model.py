from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship

from app.core import Base


class Disciplines(Base):
    __tablename__ = "disciplines"

    id = Column(String, primary_key=True)
    name = Column(String)
    pictogram_url = Column(String)
    pictogram_url_dark = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    events = relationship('Events', back_populates='discipline')
