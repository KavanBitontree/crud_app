# Schema for FuelEntry
from pydantic import BaseModel,Field
#change date to datetime as changed in models
from datetime import datetime

class FuelEntryBase(BaseModel):
    car_id: int = Field(..., description="ID of the car associated with this fuel entry")
    liters: float = Field(..., gt=0, description="Amount of fuel added in liters")
    kilometers: float = Field(..., gt=0, description="Distance driven since last refill in kilometers")
    # date_of_fuel_entry:datetime  = Field(..., description="Date of the fuel entry")

class FuelEntryCreate(FuelEntryBase):
    pass

class FuelEntryUpdate(BaseModel):
    liters: float | None = Field(None, gt=0, description="Amount of fuel added in liters")
    kilometers: float | None = Field(None, gt=0, description="Distance driven since last refill in kilometers")
    # date_of_fuel_entry: datetime | None = Field(None, description="Date of the fuel entry")

class FuelEntryResponse(FuelEntryBase):
    id: int
    car_id: int
    date_of_fuel_entry: datetime

    class Config:
        from_attributes = True
