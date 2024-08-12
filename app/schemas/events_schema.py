from datetime import datetime

from pydantic import BaseModel


class EventsBase(BaseModel):
    id: str
    day: datetime
    discipline_name: str
    discipline_pictogram: str
    name: str
    venue_name: str
    event_name: str
    detailed_event_name: str
    start_date: datetime
    end_date: datetime
    status: str
    is_medal_event: bool
    is_live: bool
    gender_code: str


class EventsCreate(EventsBase):
    pass


class EventsUpdate(EventsBase):
    pass
