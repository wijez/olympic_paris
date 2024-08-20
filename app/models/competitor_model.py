from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core import Base


class Competitor(Base):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)
    competitor_name = Column(String, nullable=False)
    position = Column(Integer, nullable=True)
    result_position = Column(String, nullable=True)
    result_winnerLoserTie = Column(String, nullable=True)
    result_mark = Column(Integer, nullable=True)

    event = relationship('Events', back_populates='competitors')
    country = relationship('Countries', back_populates='competitors')