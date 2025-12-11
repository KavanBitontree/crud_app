from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.car import Car
from schemas.car import CarCreate, CarUpdate, CarResponse

router = APIRouter(prefix="/cars", tags=["Cars"])

# -----------------------------
# Create a Car
# -----------------------------
@router.post("/", response_model=CarResponse, status_code=201)
def create_car(car_data: CarCreate, db: Session = Depends(get_db)):
    car = Car(**car_data.model_dump())
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

# -----------------------------
# Get all cars
# -----------------------------
@router.get("/", response_model=list[CarResponse])
def get_all_cars(db: Session = Depends(get_db)):
    return db.query(Car).all()

# -----------------------------
# Get one car by ID
# -----------------------------
@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# -----------------------------
# Update car (PUT – replace all fields)
# -----------------------------
@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, updated: CarCreate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    for key, value in updated.model_dump().items():
        setattr(car, key, value)

    db.commit()
    db.refresh(car)
    return car

# -----------------------------
# PATCH (partial update)
# -----------------------------
@router.patch("/{car_id}", response_model=CarResponse)
def patch_car(car_id: int, updated: CarUpdate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    data = updated.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(car, key, value)

    db.commit()
    db.refresh(car)
    return car

# -----------------------------
# Delete a car
# -----------------------------
@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()
    return {"message": "Car deleted successfully"}
