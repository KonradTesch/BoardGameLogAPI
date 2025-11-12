from datetime import date
from modules import User, Base, Player, Boardgame, Game_Session, Session_Player
from sqlalchemy import create_engine, text,inspect
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

def setup_database():
    Base.metadata.create_all(bind=engine)

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

setup_database()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DataManager:

    def __init__(self):
        pass

    def create_user(self, username: str, password: str):
        user = session.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Username already exists")

        new_user = User(
            username=username,
            hashed_password=bcrypt_context.hash(password))
        session.add(new_user)
        session.commit()

        return new_user

    def authenticate_user(self, username: str, password: str):
        user = session.query(User).filter(User.username == username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not bcrypt_context.verify(password, str(user.hashed_password)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

        return user

    def update_user(self, user_id: int, new_username: str):
        user = session.query(User).filter(User.id == user_id).first()
        user.username = new_username
        session.commit()

    def delete_user(self, user_id: int):
        user_to_delete = self.validate_user(user_id)

        session.delete(user_to_delete)
        session.commit()

    def validate_user(self, user_id:int):
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError("User not found")

        return user

    def get_all_users(self):
        return session.query(User).all()

    def get_user_by_id(self, user_id: int):
        user = self.validate_user(user_id)

        return user


    def create_player(self, user:User, player_name:str):
        new_player = Player(name=player_name, user_id=user.id)
        session.add(new_player)
        session.commit()

    def validate_player(self, player_id:int):
        player = session.query(Player).filter(Player.id == player_id).first()

        if not player:
            raise ValueError("Player not found")

        return player

    def update_player(self, user_id: int, player_id: int, new_name: str):
        user = self.validate_user(user_id)

        for player in user.players:
            if player.id != player_id and player.name == new_name:
                raise ValueError(f"Player {new_name} already exists")

        player = self.validate_player(player_id)

        player.name = new_name
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

    def create_session(self, game_id: int, user_id: int, date_value: date, players: list):
        new_session = Game_Session(game_id=game_id, user_id=user_id, date=date_value)
        session.add(new_session)
        session.commit()
        session.refresh(new_session)

        for player in players:
            player_id = player["id"]
            if session.query(Player).filter(Player.id == player_id).count() == 0:
                raise Exception(f"Player '{player_id}' does not exist")

            new_session_player = Session_Player(
                session_id = new_session.id,
                player_id = player_id,
                score = player["score"],
                winner = player["winner"]
            )

            session.add(new_session_player)
            session.commit()

    def validate_session(self, session_id: int) -> Game_Session:
        game_session = session.query(Game_Session).filter(Game_Session.id == session_id).first()

        if not game_session:
            raise ValueError("Game session not found")

        return game_session

    def update_session(self, session_id: int, game_id: int, date_value: date, players: list):

        game_session = self.validate_session(session_id)

        game_session.game_id = game_id
        game_session.date = date_value

        for player in players:
            player_id = player["player_id"]
            self.validate_player(player_id)

            session_player = session.query(Session_Player).filter(Session_Player.session_id == game_session.id).filter(Session_Player.player_id == player_id).first()

            if not session_player:
                new_session_player = Session_Player(
                    session_id = game_session.id,
                    player_id = player_id,
                    score = player["score"],
                    winner = player["winner"]
                )

                session.add(new_session_player)
            else:
                session_player.score = player["score"]
                session_player.winner = player["winner"]

            session.commit()



    def delete_session(self, session_id: int):
        session_to_delete = session.query(Game_Session).filter(Game_Session.id == session_id).first()
        if session_to_delete:
            session.delete(session_to_delete)
            session.commit()
            return True
        return False

    def get_session_by_id(self, session_id: int):
        game_session = session.query(Game_Session).filter(Game_Session.id == session_id).first()
        return game_session
