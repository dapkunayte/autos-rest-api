from pydantic import BaseModel


class AutoBase(BaseModel):
    brand: str
    age: int
    cost: float
    mileage: str
    is_sell: bool = True

    class Config:
        orm_mode = True


class Auto(AutoBase):
    id: int


class AutosCompare(BaseModel):
    pass
