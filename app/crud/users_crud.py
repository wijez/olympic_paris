from app.crud import CRUDBase
from app.models.user_model import User
from app.schemas.users_schema import UserCreate, UserUpdate


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    pass


users_crud = UserCRUD(User)
