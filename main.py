from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from connection import engine
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


def start_application():
    application = FastAPI()
    create_tables()
    include_router(application)
    configure_static(application)
    return application


app = start_application()
