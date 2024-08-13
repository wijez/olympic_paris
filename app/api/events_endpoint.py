import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.core import get_async_session
from app.crud import events_crud
from app.models.events_model import Events
from app.models.competitor_model import Competitor

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/{id}")
async def get_event_by_id(id: int, db: AsyncSession = Depends(get_async_session)):
    data = await events_crud.get(session=db, id=id)
    return data



