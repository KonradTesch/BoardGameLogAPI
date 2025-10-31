import logging

from modules import User, Base, Player, Boardgame, Game_Session, Session_Player
from sqlalchemy import create_engine, text
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

    def create_game(self, game_title: str,min_players: int, max_players:int ):
        new_game = Boardgame(title=game_title, min_players=min_players, max_players=max_players)
        if session.query(Boardgame).filter(Boardgame.title == game_title).count() > 0:
            print(f"Boardgame '{game_title}' already exists")
            return

        session.add(new_game)
        session.commit()

    def get_all_games(self, sort: bool):
        games = session.query(Boardgame).all()
        if sort:
            games = sorted(games, key=lambda game: game.title)
        return games

    def create_session(self, game_id: int, date: str, players: list, winner: int):
        new_session = Game_Session(game_id=game_id, date=date, winner_id=winner)
        session.add(new_session)
        session.commit()
        session.refresh(new_session)

        for player in players:
            player_id = session.query(Player).filter(Player.name == player).first().id
            new_session_player = Session_Player(session_id= new_session.id,player_id=player_id, score = 0)
            session.add(new_session_player)
            session.commit()
