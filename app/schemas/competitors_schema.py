from pydantic import BaseModel


class CompetitorsBase(BaseModel):
    id: int
    event_id: str
    country_id: int
    competitor_name: str
    position: str
    result_position: str
    result_winnerLoserTie: str
    result_mark: int

    class Config:
        from_attributes = True


class CompetitorsCreate(CompetitorsBase):
    pass


class CompetitorsUpdate(CompetitorsBase):
    pass
