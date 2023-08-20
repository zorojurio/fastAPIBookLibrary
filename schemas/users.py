from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserInDataBase(BaseModel):
    username: str
    hashed_password: str
    email: str
