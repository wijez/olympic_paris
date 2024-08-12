import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core import get_async_session
from app.models.events_model import Events
from app.models.competitor_model import Competitor

router = APIRouter(prefix="/events", tags=["events"])


@router.post("")
async def get_events(db: AsyncSession = Depends(get_async_session)):
    url = "https://apis.codante.io/olympic-games/events"
    all_events = await fetch_all_events(url)

    for event in all_events:
        try:
            day = datetime.fromisoformat(event["day"]).replace(tzinfo=None)
            start_date = datetime.fromisoformat(event["start_date"]).replace(tzinfo=None)
            end_date = datetime.fromisoformat(event["end_date"]).replace(tzinfo=None)

            is_medal_event = bool(event["is_medal_event"])
            is_live = bool(event["is_live"])

            db_event = Events(
                id=event["id"],
                day=day,
                discipline_name=event["discipline_name"],
                discipline_pictogram=event["discipline_pictogram"],
                name=event.get("name"),
                venue_name=event["venue_name"],
                event_name=event["event_name"],
                detailed_event_name=event.get("detailed_event_name"),
                start_date=start_date,
                end_date=end_date,
                status=event["status"],
                is_medal_event=is_medal_event,
                is_live=is_live,
                gender_code=event.get("gender_code")
            )

            db.add(db_event)

            # Handle competitors
            for competitor in event["competitors"]:
                db_competitor = Competitor(
                    event_id=db_event.id,
                    country_id=competitor["country_id"],
                    country_flag_url=competitor.get("country_flag_url"),
                    competitor_name=competitor["competitor_name"],
                    position=competitor.get("position"),
                    result_position=competitor.get("result_position", None),
                    result_winnerLoserTie=competitor["result_winnerLoserTie"],
                    result_mark=int(competitor["result_mark"]) if competitor["result_mark"].isdigit() else None
                )

                db.add(db_competitor)
            await db.commit()

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Failed to process event {event['id']}: {str(e)}")

    return {"status": "success", "data": all_events}


async def fetch_all_events(url: str) -> list:
    events = []
    async with httpx.AsyncClient() as client:
        while url:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to fetch data")

            data = response.json()
            events.extend(data.get("data", []))

            meta = data.get("meta", {})
            next_page = meta.get("current_page", 1) + 1
            last_page = meta.get("last_page", 1)
            if next_page > last_page:
                break

            url = f"{meta.get('path')}?page={next_page}&per_page={meta.get('per_page', 10)}"

    return events
