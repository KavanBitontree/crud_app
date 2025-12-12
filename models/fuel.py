from sqlalchemy import Column,Integer,Float,DateTime,ForeignKey,text
from sqlalchemy.orm import relationship
from models.base import Base


class FuelEntry(Base):
    __tablename__ = "fuel_entry"

    id = Column(Integer,primary_key=True,index=True)
    car_id = Column(Integer,ForeignKey("car.id"),nullable=False)
    liters = Column(Float,nullable=False)
    kilometers = Column(Float,nullable=False)

    date_of_fuel_entry = Column(
    DateTime(timezone=True),
    server_default=text("timezone('Asia/Kolkata', now())"),
    nullable=False
    )


    # Relationship to Car
    car = relationship("Car", back_populates="fuel_entries")
