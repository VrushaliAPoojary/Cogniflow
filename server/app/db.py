# server/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from .config import settings

# Create engine (future=True for SQLAlchemy 2.0 style)
engine = create_engine(settings.DATABASE_URL, future=True, echo=False)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,  # keeps objects usable after commit
    class_=Session
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
