from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from core.logger import get_logger

templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter(include_in_schema=False)
general_pages_router.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger(__name__)


@general_pages_router.get("/")
async def home_page(request: Request):
    logger.info(f'Process started for Home Page')
    render_data = {
        'request': request,
        'my_title': 'Sign Up',
    }
    return templates.TemplateResponse('general_pages/home.html', render_data)
