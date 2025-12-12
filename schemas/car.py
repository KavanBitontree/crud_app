from pydantic import BaseModel

class CarBase(BaseModel):
    brand: str
    model: str
    year: int

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: int | None = None

class CarResponse(CarBase):
    id: int

    class Config:
        from_attributes = True
