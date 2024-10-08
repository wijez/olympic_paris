import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core import get_async_session
from app.crud import events_crud
from app.models.events_model import Events
from app.models.competitor_model import Competitor
from app.services import EventsService
from app.utils.rate_limit import rate_limit, get_httpx_client

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{id}")
async def get_event_by_id(id: int, db: AsyncSession = Depends(get_async_session),
                          httpx_client: httpx.AsyncClient = Depends(get_httpx_client),
                          _: None = Depends(rate_limit)
                          ):
    events_service = EventsService(session=db)
    data = await events_service.get_events_data(id=id)
    return data


