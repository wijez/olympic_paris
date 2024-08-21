from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.competitors_crud import competitors_crud


class CompetitorsService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_competitor_data(self, id: int):
        competitors = await competitors_crud.get(session=self.session, id=id)
        if not competitors:
            raise HTTPException(status_code=404, detail="Competitor not found")
        return competitors
