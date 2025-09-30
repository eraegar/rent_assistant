from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


def _build_engine_from_env() -> "Engine":
    """Create SQLAlchemy engine using DATABASE_URL when provided.

    Falls back to local SQLite file. Applies SQLite-specific connect args only
    when the selected URL scheme is SQLite to avoid breaking Postgres/MySQL.
    """

    database_url = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

    # sqlite requires check_same_thread=False when used in FastAPI with threads
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


engine = _build_engine_from_env()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Database dependency function"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()