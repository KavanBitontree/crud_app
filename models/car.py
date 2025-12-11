from sqlalchemy import Column, Integer, String
from models.base import Base

class Car(Base):
    __tablename__ = "car"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
