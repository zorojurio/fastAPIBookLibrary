from typing import List, Optional

from fastapi import Request


class SearchForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.search: Optional[str] = None

    async def load_data(self) -> None:
        form = await self.request.form()
        self.search = form.get("search")
