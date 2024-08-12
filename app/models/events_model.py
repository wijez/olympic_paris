from sqlalchemy.orm import relationship

from app.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean


class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    day = Column(DateTime, nullable=False)
    discipline_name = Column(String, nullable=False)
    discipline_pictogram = Column(String, nullable=True)
    name = Column(String, nullable=True)
    venue_name = Column(String, nullable=False)
    event_name = Column(String, nullable=False)
    detailed_event_name = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    is_medal_event = Column(Boolean, nullable=False)
    is_live = Column(Boolean, nullable=False)
    gender_code = Column(String, nullable=False)

    competitors = relationship('Competitor', back_populates='event')
