from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from core.logger import get_logger
from handlers.auth import get_current_user_from_token
from models.users import User

templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter(include_in_schema=False)
general_pages_router.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

logger = get_logger(__name__)


@general_pages_router.get("/",
                          dependencies=[Depends(get_current_user_from_token)])
async def home_page(
        request: Request,
        current_user: User = Depends(get_current_user_from_token)
):
    logger.debug(current_user)
    logger.info('Process started for Home Page')
    render_data = {
        'request': request,
        'my_title': 'Sign Up',
    }
    return templates.TemplateResponse('general_pages/home.html', render_data)
