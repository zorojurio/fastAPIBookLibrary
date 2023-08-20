from datetime import date

from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    publication_date: date
    isbn: str
    cover_image: str
