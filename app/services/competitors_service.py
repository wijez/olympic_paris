import json

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client as r
from app.crud.competitors_crud import competitors_crud
from app.schemas import CompetitorsBase
from app.utils import validate_and_update_cache


class CompetitorsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_competitor_data(self, id: int):
        cache_key = f"competitor:{id}"

        competitor = await competitors_crud.get(session=self.session, id=id)

        if not competitor:
            raise HTTPException(status_code=404, detail="Competitor not found")

        competitor_data = CompetitorsBase.from_orm(competitor)
        return await validate_and_update_cache(cache_key, competitor_data)
