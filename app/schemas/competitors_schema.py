from pydantic import BaseModel


class CompetitorsBase(BaseModel):
    id: int
    name: str
    country_id: int
    country_name: str
    country_flag_url: str
    country_continent: str
    discipline_id: int
    discipline_name: str
    discipline_pictogram_url: str
    discipline_pictogram_url_dark: str
    venue_id: int


class CompetitorsCreate(CompetitorsBase):
    pass


class CompetitorsUpdate(CompetitorsBase):
    pass
