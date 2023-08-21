from fastapi import HTTPException


class CustomAuthException(HTTPException):
    pass
