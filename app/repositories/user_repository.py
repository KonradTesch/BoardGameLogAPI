from _collections_abc import Sequence

import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.auth import RegisterData
from app.models import User
from app.custom_exceptions import NotFoundException, UnauthorizedException, UnprocessableException

BCRYPT_MAX_BYTES = 72

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > BCRYPT_MAX_BYTES:
        raise UnprocessableException(f"Password must not be longer than {BCRYPT_MAX_BYTES} bytes")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > BCRYPT_MAX_BYTES:
        return False
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, register_data: RegisterData) -> User:
        user = self.db.scalars(select(User).where(User.username == register_data.username)).first()
        if user:
            raise UnprocessableException(f"Username '{register_data.username}' already exists")

        new_user = User(
            username=register_data.username,
            hashed_password=hash_password(register_data.password)
        )
        self.db.add(new_user)
        self.db.commit()

        return new_user

    def authenticate_user(self, username: str, password: str) -> User:
        user: User | None = self.db.scalars(select(User).where(User.username == username)).first()

        if not user or not verify_password(password, str(user.hashed_password)):
            raise NotFoundException("Incorrect username or password")

        return user

    def update_username(self, user_id: int, new_username: str):
        user_already_exists = self.db.scalars(select(User)
                                              .where(User.id != user_id)
                                              .where(User.username == new_username)
                                              ).first()

        if user_already_exists:
            raise UnprocessableException(f"Username '{new_username}' already exists")

        user = self.db.scalars(select(User).where(User.id == user_id)).first()

        if not user:
            raise NotFoundException("User not found")

        user.username = new_username
        self.db.commit()

    def change_password(self, user_id: int, old_password: str, new_password: str):
        current_user = self.validate_user(user_id)

        if not verify_password(old_password, str(current_user.hashed_password)):
            raise UnauthorizedException("Old password is incorrect.")

        # Hash and save the new password
        current_user.hashed_password = hash_password(new_password)
        self.db.commit()

    def delete_user(self, user_id: int):
        user_to_delete = self.validate_user(user_id)

        self.db.delete(user_to_delete)
        self.db.commit()

    def validate_user(self, user_id:int) -> User:
        user = self.db.get(User, user_id)

        if not user:
            raise NotFoundException("User not found")

        return user

    def get_all_users(self) -> Sequence[User]:
        return self.db.scalars(select(User)).all()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.validate_user(user_id)

        return user
