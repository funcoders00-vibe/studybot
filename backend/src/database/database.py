import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from src.settings import settings

logger = logging.getLogger(__name__)

db_url = (settings.database_url or "").strip()

# Automatically normalize postgresql:// to postgresql+psycopg:// if psycopg3 is used
if db_url.startswith("postgresql://") and not db_url.startswith("postgresql+psycopg://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

if not db_url:
    # Graceful fallback to SQLite so serverless deployment can start and report health
    logger.warning("DATABASE_URL is not set. Falling back to local SQLite database.")
    db_url = "sqlite:///./studybot.db"

# SQLite doesn't need pool_pre_ping with default pool
connect_args = {}
if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(db_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
