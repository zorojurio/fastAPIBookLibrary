from fastapi import FastAPI, Request, responses, status
from fastapi.templating import Jinja2Templates

from core.configs import settings
from core.exceptions import CustomAuthException
from core.logger import get_logger

logger = get_logger(__name__)

templates = Jinja2Templates(directory="templates")


def add_exception_handler(app: FastAPI):
    @app.exception_handler(CustomAuthException)
    async def handle_auth_exception(
            request: Request, exc: CustomAuthException
    ):
        """
        Catch the CustomAuthException exception and return to login page if there is a problem in authentication
        :param request:
        :param exc:
        :return:
        """
        error_log = 'User Not Authenticated'
        logger.error(error_log)
        if settings.DEBUG_MODE:
            logger.error(f'Endpoint: {request.url} Method: {request.method}')
        return responses.RedirectResponse(
            "/login", status_code=status.HTTP_302_FOUND
        )

    return None
