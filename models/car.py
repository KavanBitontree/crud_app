from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    # Relationship to FuelEntry one-to-many
    fuel_entries = relationship("FuelEntry", back_populates="car", cascade="all, delete")
