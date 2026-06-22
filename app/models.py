from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

    players = relationship('Player', back_populates='user')
    board_games = relationship('BoardGame', back_populates='user')
    sessions = relationship('GameSession', back_populates='user')

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='players')
    session_players = relationship('Session_Player', back_populates='player')

class BoardGame(Base):
    __tablename__ = 'boardgames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    min_players = Column(Integer)
    max_players = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship('User', back_populates='board_games')
    sessions = relationship('GameSession', back_populates='game')

class GameSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('boardgames.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)

    game = relationship('BoardGame', back_populates='sessions')
    user = relationship('User', back_populates='sessions')
    session_players = relationship('Session_Player', back_populates='session', cascade='all, delete-orphan')


class Session_Player(Base):
    __tablename__ = 'sessions_players'
    session_id = Column(Integer, ForeignKey('sessions.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    score = Column(Integer)
    winner = Column(Boolean)

    session = relationship('GameSession', back_populates='session_players')
    player = relationship('Player', back_populates='session_players')



