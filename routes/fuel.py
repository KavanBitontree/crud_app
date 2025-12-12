from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

from models.car import Car
from models.fuel import FuelEntry

from schemas.fuel import FuelEntryCreate, FuelEntryResponse

router = APIRouter(prefix="/fuel_entries", tags=["Fuel Entries"])

# -----------------------------
# Create a Fuel Entry
# -----------------------------

@router.post("/create_fuel_entry", response_model=FuelEntryResponse, status_code=201)
def create_fuel_entry(fuel_data:FuelEntryCreate,db:Session=Depends(get_db)):
    car = db.query(Car).filter(Car.id==fuel_data.car_id).first()
    if not car:
        raise HTTPException(status_code=404,detail="Car not found for the given car_id")
    fuel_entry = FuelEntry(**fuel_data.model_dump())
    db.add(fuel_entry)
    db.commit()
    db.refresh(fuel_entry)
    return fuel_entry

# -----------------------------
# Get all Fuel Entries
# -----------------------------

@router.get("/get_all_fuel_entries", response_model=list[FuelEntryResponse])
def get_all_fuel_entries(db:Session=Depends(get_db)):
    return db.query(FuelEntry).all()

# -----------------------------
# Get one Fuel Entry by a car ID
# -----------------------------

@router.get("/get_fuel_entries_by_car_id/{car_id}", response_model=list[FuelEntryResponse])
def get_fuel_entries_by_car_id(car_id:int,db:Session=Depends(get_db)):
    car = db.query(Car).filter(Car.id==car_id).first()
    if not car:
        raise HTTPException(status_code=404,detail="Car not found")
    return db.query(FuelEntry).filter(FuelEntry.car_id==car_id).all()

# -----------------------------
# Get latest Mileage of a car by car ID
# -----------------------------

@router.get("/get_latest_mileage_by_car_id/{car_id}")
def get_latest_mileage_by_car_id(car_id: int, db: Session = Depends(get_db)):

    entries = (
        db.query(FuelEntry)
        .filter(FuelEntry.car_id == car_id)
        .order_by(FuelEntry.date_of_fuel_entry.desc())
        .limit(2)
        .all()
    )

    if len(entries) < 2:
        raise HTTPException(
            status_code=400, 
            detail="Not enough fuel entries to calculate mileage"
        )

    latest = entries[0]
    previous = entries[1]

    # --- VALIDATION CHECKS ---

    # 1. Odometer must increase
    if latest.kilometers <= previous.kilometers:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fuel entries: odometer went backward or did not increase "
                   f"(previous={previous.kilometers}, latest={latest.kilometers})."
        )

    # 2. Liters must be positive
    if latest.liters <= 0:
        raise HTTPException(
            status_code=400,
            detail="Liters must be greater than zero"
        )

    # --- CALCULATE ---
    distance = latest.kilometers - previous.kilometers
    mileage = distance / latest.liters

    return {
        "car_id": car_id,
        "latest_mileage_km_per_liter": round(mileage, 2),
        "distance_driven_km": distance,
        "liters_filled": latest.liters
    }

# -----------------------------
# Delete a Fuel Entry
# -----------------------------

@router.delete("/delete_fuel_entry_by_id/{fuel_entry_id}")
def delete_fuel_entry_by_id(fuel_entry_id:int,db:Session=Depends(get_db)):
    fuel_entry = db.query(FuelEntry).filter(FuelEntry.id==fuel_entry_id).first()
    if not fuel_entry:
        raise HTTPException(status_code=404,detail="Fuel Entry not found")
    db.delete(fuel_entry)
    db.commit()
    return {"detail":"Fuel Entry deleted successfully"}
