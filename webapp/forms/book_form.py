from datetime import date
from typing import List, Optional

from fastapi import Request


class BookForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.title: Optional[str] = None
        self.author: Optional[str] = None
        self.publication_date: Optional[date] = None
        self.isbn: Optional[str] = None

    async def load_data(self) -> None:
        form = await self.request.form()
        self.title = form.get("title")
        self.author = form.get("author")
        self.publication_date = form.get("publication_date")
        self.isbn = form.get("isbn")

    async def is_valid(self) -> bool:
        if not self.title:
            self.errors.append("Title is a mandatory Field")
        if not self.author:
            self.errors.append("Author is a mandatory Field")
        if not self.errors:
            return True
        return False
