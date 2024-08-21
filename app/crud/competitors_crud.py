from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Competitor
from app.schemas import CompetitorsCreate, CompetitorsUpdate


class CompetitorsCRUD(CRUDBase[Competitor, CompetitorsCreate, CompetitorsUpdate]):

    # def __init__(self, model):
    #     super().__init__(model)

    async def get_competitors_by_event_id(self, event_id: str, session: AsyncSession):
        competitors = await self.get_all(event_id=event_id, session=session)
        return competitors


competitors_crud = CompetitorsCRUD(Competitor)
