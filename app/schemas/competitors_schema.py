from datetime import datetime

from pydantic import BaseModel


class CompetitorsBase(BaseModel):
    id: int
    event_id: int
    country_id: str
    competitor_name: str
    position: int
    result_position: str = None
    result_winnerLoserTie: str = None
    result_mark: int = None

    class Config:
        from_attributes = True


class CompetitorsCreate(CompetitorsBase):
    created_at: datetime


class CompetitorsUpdate(CompetitorsBase):
    updated_at: datetime
