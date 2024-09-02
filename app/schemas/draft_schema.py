from uuid import UUID

from pydantic import BaseModel

from app.utils import DraftStatus


class DraftCreate(BaseModel):
    title: str
    content: str


class DraftUpdate(BaseModel):
    title: str
    content: str


class DraftResponse(BaseModel):
    id: UUID
    title: str
    content: str
    user_id: UUID
    status: DraftStatus
