import logging

from modules import User, Base, Player
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import contextlib
import os

def setup_database():
    Base.metadata.create_all(bind=engine)

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

setup_database()


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

    def get_user_by_id(self, user_id: int):
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return user

        return None

    def create_user_player(self, user:User, player_name:str):
        new_player = Player(name=player_name, user_id=user.id)
        session.add(new_player)
        session.commit()

    def delete_player(self, player_id: int):
        player_to_delete = session.query(Player).filter(Player.id == player_id)
        if player_to_delete:
            player_to_delete.delete()
            session.commit()
            return True
        return False
