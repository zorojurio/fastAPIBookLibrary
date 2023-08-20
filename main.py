from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from connection import engine
from models import users
from webapp.routes.route_homepage import general_pages_router
from webapp.routes.user_auth import auth

users.Base.metadata.create_all(bind=engine)


def include_router(application):
    application.include_router(general_pages_router)
    application.include_router(auth)


def configure_static(application):
    application.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    application = FastAPI()
    include_router(application)
    configure_static(application)
    return application


app = start_application()
