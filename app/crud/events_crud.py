from app.crud import CRUDBase
from app.models.events_model import Events
from app.schemas.events_schema import EventsCreate, EventsUpdate


class EventsCRUD(CRUDBase[Events, EventsCreate, EventsUpdate]):
    pass
