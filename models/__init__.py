from .base import Base

# import all models so Alembic can discover them
from .car import Car
from .fuel import FuelEntry

__all__ = ["Base", "Car", "FuelEntry"]