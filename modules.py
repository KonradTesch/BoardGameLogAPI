from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    players = relationship('Player')

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

class Boardgame(Base):
    __tablename__ = 'boardgames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    min_players = Column(Integer)
    max_players = Column(Integer)


class Game_Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('boardgames.id'))
    date = Column(String)
    winner_id = Column(Integer, ForeignKey('players.id'))

    winner = relationship("Player")

class Session_Player(Base):
    __tablename__ = 'sessions_players'
    session_id = Column(Integer, ForeignKey('sessions.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    score = Column(Integer)



