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
        competitors_data = []
        for competitor in competitors:
            competitors_data.append({
                "id": competitor.id,
                "event_id": competitor.event_id,
                "country_name": competitor.country.name,
                "country_flag_url": competitor.country.flag_url,
                "competitor_name": competitor.competitor_name,
                "position": competitor.position,
                "result_position": competitor.result_position,
                "result_winnerLoserTie": competitor.result_winnerLoserTie,
                "result_mark": competitor.result_mark
            })

        data = {
            "events": events,
            "competitors": competitors_data
        }
        return data
