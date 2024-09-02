from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, username: str):
        query = select(User).filter_by(username=username)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str):
        query = select(User).filter_by(email=email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update_user_password(self, user: User, new_password: str):
        user.hashed_password = new_password
        self.session.add(user)
        await self.session.commit()
