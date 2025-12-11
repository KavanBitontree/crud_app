from .base import Base

# import all models so Alembic can discover them
from .car import Car

__all__ = ["Base", "Car"]