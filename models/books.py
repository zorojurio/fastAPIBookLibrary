from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import func, DateTime, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from connection import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False, index=True)
    author = Column(Text, nullable=False, index=True)
    publication_date = Column(Date, nullable=True)
    isbn = Column(Text, nullable=True, unique=True)
    cover_image = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User")
