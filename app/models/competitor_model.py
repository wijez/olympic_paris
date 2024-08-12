from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core import Base


class Competitor(Base):
    __tablename__ = 'competitors'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    country_id = Column(String, nullable=False)
    country_flag_url = Column(String, nullable=True)
    competitor_name = Column(String, nullable=False)
    position = Column(Integer, nullable=True)
    result_position = Column(String, nullable=True)
    result_winnerLoserTie = Column(String, nullable=False)
    result_mark = Column(Integer, nullable=False)

    event = relationship('Events', back_populates='competitors')