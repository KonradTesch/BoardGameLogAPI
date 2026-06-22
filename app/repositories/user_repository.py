from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import User
from app.custom_exceptions import NotFoundException, UnauthorizedException, UnprocessableException

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            raise UnprocessableException(f"Username '{username}' already exists")

        new_user = User(
            username=username,
            hashed_password=bcrypt_context.hash(password))
        self.db.add(new_user)
        self.db.commit()

        return new_user

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()

        if not user:
            raise NotFoundException(f"Username '{username}' not found")
        if not bcrypt_context.verify(password, str(user.hashed_password)):
            raise UnauthorizedException("Incorrect password")

        return user

    def update_username(self, user_id: int, new_username: str):
        user = self.db.query(User).filter(User.id == user_id).first()
        user.username = new_username
        self.db.commit()

    def change_password(self, user_id: int, old_password: str, new_password: str):
        current_user = self.validate_user(user_id)

        if not bcrypt_context.verify(old_password, str(current_user.hashed_password)):
            raise UnauthorizedException("Old password is incorrect.")

        # Hash and save the new password
        current_user.hashed_password = bcrypt_context.hash(new_password)
        self.db.commit()

    def delete_user(self, user_id: int):
        user_to_delete = self.validate_user(user_id)

        self.db.delete(user_to_delete)
        self.db.commit()

    def validate_user(self, user_id:int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise NotFoundException("User not found")

        return user

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.validate_user(user_id)

        return user
