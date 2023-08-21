from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from connection import get_db, Session
from core.logger import get_logger
from handlers.auth import get_current_user_from_token
from handlers.book import BookHandler
from models.users import User

templates = Jinja2Templates(directory="templates")
general_pages_router = APIRouter(include_in_schema=False)

logger = get_logger(__name__)


@general_pages_router.get(
    "/",
    dependencies=[Depends(get_current_user_from_token)])
async def home_page(
        request: Request,
        current_user: User = Depends(get_current_user_from_token),
        db: Session = Depends(get_db)):
    logger.info('Process started for Dashboard')
    book_handler = BookHandler(db)
    total_books = book_handler.total_books_by_user(current_user.id)
    recent_books, recent_book_count = book_handler.recent_books_by_user(current_user.id)
    render_data = {
        'request': request,
        'my_title': 'Sign Up',
        'total_books': total_books,
        'recent_book_count': recent_book_count,
        'recent_books': recent_books
    }
    return templates.TemplateResponse('general_pages/home.html', render_data)
