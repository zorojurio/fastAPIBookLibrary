from typing import Dict
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError

from connection import Session, get_db
from core.configs import settings
from core.exceptions import CustomAuthException
from core.logger import get_logger
from handlers.user import UserHandler

logger = get_logger(__name__)


class CustomHeaderCookieAuth(OAuth2):
    def __init__(
            self,
            token_url: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": token_url, "scopes": scopes}
        )
        super().__init__(flows=flows,
                         scheme_name=scheme_name,
                         auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )
        scheme, param = '', ''
        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise CustomAuthException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = CustomHeaderCookieAuth(token_url="token")


def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = CustomAuthException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        logger.debug(f"username extracted is {username}")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_handler = UserHandler(session=db)
    user = user_handler.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user
