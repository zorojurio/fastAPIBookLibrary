from fastapi import APIRouter, Request, responses, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from core.logger import get_logger
from connection import Session, get_db
from handlers.hasher import Hasher
from handlers.user import UserHandler
from schemas.users import UserCreate
from webapp.users.form import UserCreateForm

templates = Jinja2Templates(directory="templates")
auth = APIRouter()
auth.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger(__name__)


@auth.get("/login")
async def sign_in(request: Request):
    logger.info(f'Process started for Login Page')
    render_data = {
        'request': request,

    }
    return templates.TemplateResponse('auth/sign_in_page.html', render_data)


@auth.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    logger.info(f'Process started for Get Sign Up Page')
    render_data = {
        'request': request,

    }
    return templates.TemplateResponse('auth/sign_up_page.html', render_data)


@auth.post("/register")
async def register(request: Request,  db: Session = Depends(get_db)):
    logger.info(f'Process started for Sign Up User')
    user_create_form = UserCreateForm(request)
    logger.debug(f'{user_create_form.__dict__}')
    await user_create_form.load_data()
    if await user_create_form.is_valid():
        hashed_password = Hasher.hash_password(user_create_form.password)
        user = UserCreate(
            username=user_create_form.username, email=user_create_form.email, password=hashed_password
        )
        logger.debug(f'Form is Successfully Validated {user.__dict__}')
        try:
            UserHandler.create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            user_create_form.__dict__.get("errors").append("Duplicate username or email")
    return templates.TemplateResponse("auth/sign_up_page.html", user_create_form.__dict__)

