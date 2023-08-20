from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.configs import settings

other_args = {'connect_timeout': 240}

engine = create_engine(settings.DATABASE_URL, echo=False, max_overflow=100,
                       pool_size=100, pool_timeout=20, pool_recycle=299, connect_args=other_args, pool_pre_ping=True)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


def get_db():
    """Create session for database connection"""
    session = Session()
    try:
        yield session
    finally:
        session.close()
