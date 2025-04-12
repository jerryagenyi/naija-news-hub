"""
Database connection module for Naija News Hub.

This module provides functions to connect to the database and create sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from typing import Generator

from config.config import get_config
from src.database.models import Base

def get_connection_string() -> str:
    """
    Get the database connection string from the configuration.
    
    Returns:
        str: Database connection string
    """
    config = get_config()
    db_config = config.database
    
    return f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"

def create_database_engine():
    """
    Create a SQLAlchemy engine for the database.
    
    Returns:
        Engine: SQLAlchemy engine
    """
    config = get_config()
    db_config = config.database
    
    connection_string = get_connection_string()
    
    return create_engine(
        connection_string,
        poolclass=QueuePool,
        pool_size=db_config.pool_size,
        max_overflow=db_config.max_overflow,
        pool_pre_ping=True,
    )

# Create a global engine
engine = create_database_engine()

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Get a database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)
