from pydantic import BaseModel


class VenuesBase(BaseModel):
    id: str
    name: str
    url: str


class VenuesUpdate(VenuesBase):
    pass

class VenuesCreate(VenuesBase):
    pass