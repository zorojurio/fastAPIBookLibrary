from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from connection import engine
from core.configs import settings
from exception_handler import add_exception_handler
from models import users, books
from webapp.routes.books import books_router
from webapp.routes.route_homepage import general_pages_router
from webapp.routes.user_auth import auth


def create_tables():
    users.Base.metadata.create_all(bind=engine)
    books.Base.metadata.create_all(bind=engine)


def include_router(application):
    application.include_router(general_pages_router)
    application.include_router(auth)
    application.include_router(books_router)


def configure_static(application):
    application.mount(
        "/static",
        StaticFiles(directory="static"),
        name="static"
    )
    application.mount(
        "/images",
        StaticFiles(directory="images"),
        name="images"
    )


def start_application():
    application = FastAPI()
    create_tables()
    application.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY
    )
    include_router(application)
    configure_static(application)
    add_exception_handler(application)
    return application


app = start_application()
