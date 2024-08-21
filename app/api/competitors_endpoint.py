from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.services import CompetitorsService

router = APIRouter(prefix="/competitors", tags=["competitors"])


@router.get("/{id}")
async def get_competitors(id: int, db: AsyncSession = Depends(get_async_session)):
    competitors_service = CompetitorsService(session=db)
    data = await competitors_service.get_competitor_data(id=id)
    return data
