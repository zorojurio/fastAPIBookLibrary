from fastapi import APIRouter, Depends, Request, File, UploadFile, responses
from pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from connection import Session, get_db
from core.configs import settings
from core.logger import get_logger
from handlers.auth import get_current_user_from_token
from handlers.book import BookHandler
from models.users import User
from schemas.books import BookCreate
from webapp.forms.book_form import BookForm
from webapp.forms.search_form import SearchForm

templates = Jinja2Templates(directory="templates")
books_router = APIRouter(include_in_schema=False, prefix='/books')
books_router.mount("/static", StaticFiles(directory="static"), name="static")

logger = get_logger(__name__)


@books_router.get("/create",
                  response_class=HTMLResponse,
                  dependencies=[Depends(get_current_user_from_token)]
                  )
async def create_book_get(request: Request, ):
    logger.info('Process started for Get Book Create Page')
    render_data = {
        'request': request,
        'page_type': 'Create Book'
    }
    return templates.TemplateResponse('books/book_create.html', render_data)


@books_router.post('/create',
                   dependencies=[Depends(get_current_user_from_token)])
async def create_book(request: Request,
                      cover_image: UploadFile = File(),
                      current_user: User = Depends(
                          get_current_user_from_token
                      ),
                      db: Session = Depends(get_db)):
    logger.debug(f'{cover_image.filename}')
    book_form = BookForm(request)
    await book_form.load_data()
    logger.debug(f'{book_form.__dict__}')

    if await book_form.is_valid():
        try:
            image_path = None
            if cover_image.filename:
                file_content = await cover_image.read()
                image_path = f".{settings.IMAGE_DIR}/{cover_image.filename}"
                logger.debug(f'Saving image in {image_path}')
                with open(image_path, 'wb') as file:
                    file.write(file_content)
                image_path = cover_image.filename
            book = BookCreate(
                title=book_form.title,
                author=book_form.author,
                publication_date=book_form.publication_date
                if book_form.publication_date else None,
                isbn=book_form.isbn if book_form.isbn else None,
                cover_image=image_path,
                user_id=current_user.id
            )

            logger.debug(f"BookCreate {book.__dict__}")
            book_handler = BookHandler(session=db)
            book_handler.create_new_book(book)
            return responses.RedirectResponse(
                "/books/list", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError as i:
            logger.error(f'Duplicate auther or title {i}')
            (book_form.__dict__.get("errors").
             append("Duplicate auther or title or Isbn"))
        except ValidationError as ve:
            logger.error(f"{ve.errors()[0].get('msg')}")
            (book_form.__dict__.get("errors").
             append(f"{ve.errors()[0].get('msg')}"))
        except Exception as e:
            logger.error(f'Error Occurred {e}')
            (book_form.__dict__.get("errors").
             append('Something went wrong please contact support'))
        return templates.TemplateResponse(
            "books/book_create.html",
            book_form.__dict__
        )


@books_router.get("/list",
                  response_class=HTMLResponse,

                  dependencies=[Depends(get_current_user_from_token)])
async def create_book_post(request: Request,
                           current_user: User = Depends(
                               get_current_user_from_token
                           ),
                           db: Session = Depends(get_db)):
    logger.info('Process started for Get Book List Page')

    book_handler = BookHandler(session=db)
    books = book_handler.get_book_list(current_user.id)
    render_data = {
        'request': request,
        'books': books
    }
    return templates.TemplateResponse(
        'books/book_list.html',
        render_data
    )


@books_router.get("/{book_id}",
                  response_class=HTMLResponse,

                  dependencies=[Depends(get_current_user_from_token)])
async def view_book_get(request: Request,
                        book_id: str,
                        current_user: User = Depends(
                            get_current_user_from_token
                        ),
                        db: Session = Depends(get_db)):
    logger.info('Process started for Get Book List Page')

    book_handler = BookHandler(session=db)
    book = book_handler.book_by_userid_book_id(
        current_user.id, book_id=book_id)
    render_data = {
        'request': request,
        'book': book
    }
    return templates.TemplateResponse(
        'books/book_detail.html',
        render_data
    )


@books_router.get("/update/{book_id}",
                  response_class=HTMLResponse,
                  dependencies=[Depends(get_current_user_from_token)]
                  )
async def update_book_get(book_id: str,
                          request: Request,
                          current_user: User = Depends(
                              get_current_user_from_token),
                          db: Session = Depends(get_db)):
    logger.info('Process started for Get Book Update Page')
    book_handler = BookHandler(session=db)
    book = book_handler.book_by_userid_book_id(
        current_user.id, book_id=book_id)
    render_data = {
        'request': request,
        'page_type': 'Update Book',
        'book': book

    }
    return templates.TemplateResponse('books/book_update.html', render_data)


@books_router.patch("/update/{book_id}",
                    response_class=HTMLResponse,
                    dependencies=[Depends(get_current_user_from_token)]
                    )
async def update_book_put(book_id: str,
                          request: Request,
                          cover_image: UploadFile = File(),
                          db: Session = Depends(get_db)):
    logger.info('Process started for Put Book Update Page')
    book_form = BookForm(request)
    await book_form.load_data()
    logger.debug(f'{book_form.__dict__}')
    if await book_form.is_valid():
        try:
            image_path = None
            if cover_image.filename:
                file_content = await cover_image.read()
                image_path = f".{settings.IMAGE_DIR}/{cover_image.filename}"
                logger.debug(f'Saving image in {image_path}')
                with open(image_path, 'wb') as file:
                    file.write(file_content)
                image_path = cover_image.filename
            book_handler = BookHandler(session=db)
            book_data = book_handler.prepare_update_data(book_form, image_path)
            book_handler.update_book(book_data, book_id)
            logger.debug(f"Book Update {book_data}")
            return responses.RedirectResponse(
                "/books/list", status_code=status.HTTP_303_SEE_OTHER
            )
        except IntegrityError as i:
            logger.error(f'Duplicate auther or title {i}')
            (book_form.__dict__.get("errors").
             append("Duplicate auther or title or Isbn"))
        except ValidationError as ve:
            logger.error(f"{ve.errors()[0].get('msg')}")
            (book_form.__dict__.get("errors").
             append(f"{ve.errors()[0].get('msg')}"))
        except Exception as e:
            logger.error(f'Error Occurred {e}')
            (book_form.__dict__.get("errors").
             append('Something went wrong please contact support'))
        return templates.TemplateResponse(
            "books/book_update.html",
            book_form.__dict__
        )
    return templates.TemplateResponse(
        "books/book_update.html",
        book_form.__dict__
    )


@books_router.delete("/delete/{book_id}",
                     response_class=HTMLResponse,
                     dependencies=[Depends(get_current_user_from_token)]
                     )
async def delete_book_put(book_id: str,
                          db: Session = Depends(get_db)):
    logger.info('Process started for Delete Book')
    book_handler = BookHandler(session=db)
    book_handler.delete_book(book_id)


@books_router.get("/search/author",
                  response_class=HTMLResponse,
                  dependencies=[Depends(get_current_user_from_token
                                        )])
async def search_book_get(request: Request):
    render_data = {
        'request': request,
        'books': None
    }
    return templates.TemplateResponse(
        "books/book_search.html",
        render_data
    )


@books_router.post("/search/author",
                   response_class=HTMLResponse,
                   dependencies=[Depends(get_current_user_from_token)]
                   )
async def search_book_post(
        request: Request,
        db: Session = Depends(get_db)
):
    form = SearchForm(request)
    await form.load_data()
    book_handler = BookHandler(session=db)
    books = book_handler.find_by_title_or_author(form.search)
    render_data = {
        'request': request,
        'books': books
    }
    return templates.TemplateResponse(
        "books/book_search.html",
        render_data
    )
