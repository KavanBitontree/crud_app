from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base  # <-- important: use your existing Base

# Your PostgreSQL URL
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/cars"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal class → each request gets its own DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
