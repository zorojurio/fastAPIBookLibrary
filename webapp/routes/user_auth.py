from fastapi import APIRouter, Request, responses, Depends
from fastapi.templating import Jinja2Templates
from pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from core.logger import get_logger
from connection import Session, get_db
from handlers.hasher import Hasher
from handlers.token import create_access_token
from handlers.user import UserHandler
from schemas.users import UserCreate, UserLogin
from webapp.forms.login_form import LoginForm
from webapp.forms.register_form import UserCreateForm

templates = Jinja2Templates(directory="templates")
auth = APIRouter(include_in_schema=False)
auth.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger(__name__)


@auth.get("/login", response_class=HTMLResponse)
async def sign_in(request: Request):
    logger.info(f'Process started for Get Login Page')
    render_data = {
        'request': request,

    }
    return templates.TemplateResponse('auth/sign_in_page.html', render_data)


@auth.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    logger.info(f'Process started for Post Login Page')
    login_form = LoginForm(request)
    await login_form.load_data()
    logger.debug(f'{login_form.__dict__}')
    if await login_form.is_valid():
        user = UserLogin(
            username=login_form.username, password=login_form.password
        )
        user_handler = UserHandler(session=db)
        auth_user = user_handler.authenticate_user(user)
        if auth_user:
            logger.debug(f'{user.username} Authenticated Successfully')
            response = responses.RedirectResponse(
                "/", status_code=status.HTTP_302_FOUND
            )
            token = create_access_token({'sub': login_form.username})
            response.set_cookie(
                key="Authorization", value=f"Bearer {token}", httponly=True
            )
            return response
        else:
            logger.debug(f'{user.username} Authentication Failed')
            login_form.errors.append('Invalid Username or Password')
    return templates.TemplateResponse("auth/sign_in_page.html", login_form.__dict__)


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
    await user_create_form.load_data()
    logger.debug(f'{user_create_form.__dict__}')
    if await user_create_form.is_valid():
        try:
            hashed_password = Hasher.hash_password(user_create_form.password)
            user = UserCreate(
                username=user_create_form.username, email=user_create_form.email, password=hashed_password
            )
            logger.debug(f'Form is Successfully Validated {user.__dict__}')
            user_handler = UserHandler(session=db)
            user_handler.create_new_user(user=user)
            return responses.RedirectResponse(
                "/login", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            user_create_form.__dict__.get("errors").append("Duplicate username or email")
        except ValidationError as ve:
            user_create_form.__dict__.get("errors").append(f"{ve.errors()[0].get('msg')}")
        except Exception as e:
            logger.error(f'Error Occurred {e}')
            user_create_form.__dict__.get("errors").append('Something went wrong please contact support')
    return templates.TemplateResponse("auth/sign_up_page.html", user_create_form.__dict__)

