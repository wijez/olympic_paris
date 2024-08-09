from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Venues
from app.schemas import VenuesCreate, VenuesUpdate


class VenuesCRUD(CRUDBase[Venues, VenuesCreate, VenuesUpdate]):
    pass


venues_crud = VenuesCRUD(Venues)
