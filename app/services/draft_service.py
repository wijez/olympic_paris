from sqlalchemy.ext.asyncio import AsyncSession


class DraftService:
    def __init__(self, session: AsyncSession):
        self.session = session


