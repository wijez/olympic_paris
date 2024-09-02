from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.Depends.authorization import get_current_active_user
from app.core import get_async_session
from app.crud.draft_crud import draft_crud
from app.models.draft_model import Draft
from app.models.user_model import User
from app.schemas.draft_schema import DraftCreate, DraftUpdate, DraftResponse
from app.services.draft_service import DraftService

router = APIRouter(prefix="/drafts", tags=["drafts"])


@router.post("/create", response_model=DraftResponse)
async def create_draft(draft: DraftCreate,
                       current_user: Annotated[User, Depends(get_current_active_user)],
                       db: AsyncSession = Depends(get_async_session),
                       ):
    draft_data = draft.dict()
    draft_data['user_id'] = current_user.id

    result = await draft_crud.create(db, draft_data)
    return result


@router.post("/update")
async def update_draft(draft_id: int, draft: DraftUpdate,
                       current_user: Annotated[User, Depends(get_current_active_user)],
                       db: AsyncSession = Depends(get_async_session),
                       ):
    existing_draft = await draft_crud.get(db, id=draft_id)
    # result = await db.execute(select(Draft).filter(Draft.id == draft_id))
    # existing_draft = result.scalars().first()

    if not existing_draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    if existing_draft.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this draft")
    # existing_draft.title = draft.title
    # existing_draft.content = draft.content
    #
    # await db.commit()
    # await db.refresh(existing_draft)
    updated_draft = await draft_crud.update(db, obj_in=draft, id=draft_id)
    return updated_draft
