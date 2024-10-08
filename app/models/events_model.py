from sqlalchemy.orm import relationship

from app.core import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func


class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    day = Column(DateTime, nullable=False)
    # discipline_name = Column(String, nullable=False)
    # discipline_pictogram = Column(String, nullable=True)
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

    discipline_id = Column(String, ForeignKey("disciplines.id"), nullable=False)
    venue_id = Column(String, ForeignKey("venues.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    venue = relationship("Venues", back_populates="events")
    discipline = relationship('Disciplines', back_populates='events')
    competitors = relationship('Competitor', back_populates='event')
