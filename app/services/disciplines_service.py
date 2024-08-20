from sqlalchemy.ext.asyncio import AsyncSession


class DisciplinesService:

    def __init__(self, session: AsyncSession):
        self.session = session
