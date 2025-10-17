from modules import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

def setup_database():
    Base.metadata.create_all(bind=engine)

class DataManager:

    def __init__(self):
        pass

    def create_user(self, name: str):
        new_user = User(name=name)
        session.add(new_user)
        session.commit()

    def delete_user(self, index: int):
        user_to_delete = session.query(User).filter(User.id == index)
        if user_to_delete:
            user_to_delete.delete()
            session.commit()
            return True

        return False

    def get_all_users(self):
        return session.query(User).all()



