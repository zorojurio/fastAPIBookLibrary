from fastapi import APIRouter, Depends, Request, File, UploadFile, responses
from pydantic_core import ValidationError
from starlette import status
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from connection import Session, get_db
from core.configs import settings
from core.logger import get_logger
from handlers.book import BookHandler
from models.users import User

from handlers.auth import get_current_user_from_token
from schemas.books import BookCreate
from webapp.forms.book_form import BookForm

templates = Jinja2Templates(directory="templates")
books_router = APIRouter(include_in_schema=False, prefix='/books')
books_router.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger(__name__)


@books_router.get("/create", response_class=HTMLResponse, dependencies=[Depends(get_current_user_from_token)])
async def create_book_get(request: Request, ):
    logger.info(f'Process started for Get Login Page')
    render_data = {
        'request': request,
        'page_type': 'Create Book'
    }
    return templates.TemplateResponse('books/book_create.html', render_data)


@books_router.post('/create', dependencies=[Depends(get_current_user_from_token)])
async def create_book(request: Request, cover_image: UploadFile = File(),
                current_user: User = Depends(get_current_user_from_token),
                db: Session = Depends(get_db)):
    logger.debug(f'{cover_image.filename}')
    book_form = BookForm(request)
    await book_form.load_data()
    logger.debug(f'{book_form.__dict__}')

    if await book_form.is_valid():
        try:
            file_content = await cover_image.read()
            image_path = f".{settings.IMAGE_DIR}/{cover_image.filename}"
            logger.debug(f'Saving image in {image_path}')
            with open(image_path, 'wb') as file:
                file.write(file_content)

            book = BookCreate(
                title=book_form.title,
                author=book_form.author,
                publication_date=book_form.publication_date,
                isbn=book_form.isbn,
                cover_image=image_path
            )

            logger.debug(f"BookCreate {book.__dict__}")
            book_handler = BookHandler(session=db)
            book_model = book_handler.create_new_book(book)
            return responses.RedirectResponse(
                "/", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            book_form.__dict__.get("errors").append("Duplicate auther or title")
        except ValidationError as ve:
            book_form.__dict__.get("errors").append(f"{ve.errors()[0].get('msg')}")
        except Exception as e:
            logger.error(f'Error Occurred {e}')
            book_form.__dict__.get("errors").append('Something went wrong please contact support')
        return templates.TemplateResponse("books/book_create.html", book_form.__dict__)



