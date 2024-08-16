from pydantic import BaseModel

from app.utils import RoleEnum


class UserBase(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    role: RoleEnum

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            username=obj.username,
            email=obj.email,
            is_active=obj.is_active,
            role=obj.role
        )

    @classmethod
    def from_orms(cls, objs):
        return [cls.from_orm(obj) for obj in objs]


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    password: str
