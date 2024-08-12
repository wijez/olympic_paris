import httpx
import logging

import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core import get_async_session
from app.crud.venues_crud import venues_crud
from app.models import Venues
from app.services.venues_service import VenuesService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/venues", tags=["venues"])


@router.post("")
async def get_venues(db: Session = Depends(get_async_session)):
    url = "https://apis.codante.io/olympic-games/venues"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch data")

    venues_data = response.json().get("data", [])

    for venue in venues_data:
        db_venue = Venues(id=venue["id"], name=venue["name"], url=venue["url"])
        await db.merge(db_venue)
        await db.commit()

    return {"status": "success", "data": venues_data}


@router.get("/{id}")
async def get_venues(id: str, db: AsyncSession = Depends(get_async_session)):
    venues_service = VenuesService(session=db)
    data = await venues_service.get_venue_by_id(id=id)
    return data


@router.get("/url/{name}")
async def get_url_venues(name: str, db: AsyncSession = Depends(get_async_session)):
    venues_service = VenuesService(session=db)
    data = await venues_service.get_venues_url(name=name)
    return data
