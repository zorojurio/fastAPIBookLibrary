from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self) -> None:
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self) -> bool:
        if not self.username or not len(self.username) > 3:
            self.errors.append("Username should be more than 3 chars")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be more than 4 chars")
        if not self.errors:
            return True
        return False
