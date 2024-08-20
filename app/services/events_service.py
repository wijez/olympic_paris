from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import events_crud
from app.crud.competitors_crud import competitors_crud


class EventsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_events_data(self, id: int):
        events = await events_crud.get(session=self.session, id=id)
        if not events:
            raise HTTPException(status_code=404, detail="Event not found")
        competitors = await competitors_crud.get_competitors_by_event_id(session=self.session, event_id=id)
        data = {
            "events": events,
            "competitors": competitors
        }
        return data



