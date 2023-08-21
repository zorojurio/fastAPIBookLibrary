from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    publication_date: Optional[date]
    isbn: Optional[str]
    cover_image: Optional[str]
    user_id: int


class BooksList(BookCreate):
    id: int


class BookUpdate(BooksList):
    pass
