

from sqlalchemy import Boolean, func, DateTime, Text
from sqlalchemy import Column
from sqlalchemy import Integer

from connection import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False)
    email = Column(Text, nullable=False, unique=True, index=True)
    hashed_password = Column(Text, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

