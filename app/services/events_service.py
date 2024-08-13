from sqlalchemy.ext.asyncio import AsyncSession


class EventsService:

    def __init__(self, session: AsyncSession):
        self.session = session


