from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core import Base


class Disciplines(Base):
    __tablename__ = "disciplines"

    id = Column(String, primary_key=True)
    name = Column(String)
    pictogram_url = Column(String)
    pictogram_url_dark = Column(String)

    events = relationship('Events', back_populates='discipline')
