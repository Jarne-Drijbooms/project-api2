from pydantic import BaseModel


class SingleBase(BaseModel):
    hoogste_positie: int
    huidige_positie: int


class SingleCreate(SingleBase):
    hoogste_positie: int
    huidige_positie: int


class Single(SingleBase):
    id: int
    enkelspel_id: int

    class Config:
        orm_mode = True

class Dubblebase(BaseModel):
    hoogste_positie: int
    huidige_positie: int

class DubbleCreate(SingleBase):
    hoogste_positie: int
    huidige_positie: int


class Dubble(SingleBase):
    id: int
    dubbelspel_id: int

    class Config:
        orm_mode = True

class PlayerBase(BaseModel):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str

class PlayerCreate(PlayerBase):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str


class Player(PlayerBase):
    id: int
    is_active: bool
    enkelspel: list[Single] = []
    dubbelspel: list[Dubble] = []

    class Config:
        orm_mode = True