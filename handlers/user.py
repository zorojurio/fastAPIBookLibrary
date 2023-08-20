from connection import Session
from handlers.hasher import Hasher
from models.users import User
from schemas.users import UserCreate, UserLogin, UserInDataBase


class UserHandler:
    def __init__(self, session: Session):
        self.session = session

    def create_new_user(self, user: UserCreate):
        user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password,
            is_active=True,
            is_superuser=False,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_username(self, username: str):
        user = self.session.query(User).filter(User.username == username).first()
        if user:
            user_data = UserInDataBase(**user.__dict__)
            return user_data
        return None

    def authenticate_user(self, user: UserLogin):
        existing_user = self.get_user_by_username(username=user.username)
        if not existing_user:
            return False
        if not Hasher.verify_password(plain_password=user.password, hashed_password=existing_user.hashed_password):
            return False
        return existing_user
