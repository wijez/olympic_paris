from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.core import Base


class Countries(Base):
    __tablename__ = "countries"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    continent = Column(String, nullable=False)
    flag_url = Column(String, nullable=True)
    gold_medals = Column(Integer, nullable=False)
    silver_medals = Column(Integer, nullable=False)
    bronze_medals = Column(Integer, nullable=False)
    total_medals = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    rank_total_medals = Column(Integer, nullable=False)

    competitors = relationship('Competitor', back_populates='country', lazy="selectin")
