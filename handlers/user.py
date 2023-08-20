from connection import Session
from models.users import User
from schemas.users import UserCreate


class UserHandler:

    @staticmethod
    def create_new_user(user: UserCreate, db: Session):
        user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password,
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        return user
