from app.crud import CRUDBase
from app.models.draft_model import Draft
from app.schemas.draft_schema import DraftCreate, DraftUpdate


class DraftCRUD(CRUDBase[Draft, DraftCreate, DraftUpdate]):
    pass


draft_crud = DraftCRUD(Draft)
