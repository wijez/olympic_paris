from pydantic import BaseModel


class DisciplinesBase(BaseModel):
    name: str
    pictogram_url: str
    pictogram_url_dark: str

    class Config:
        from_attributes = True


class DisciplinesCreate(DisciplinesBase):
    pass


class DisciplinesUpdate(DisciplinesBase):
    pass
