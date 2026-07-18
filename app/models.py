from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    players = relationship('Player', back_populates='user')
    board_games = relationship('BoardGame', back_populates='user')
    sessions = relationship('GameSession', back_populates='user')

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='players')
    session_players = relationship('SessionPlayer', back_populates='player', cascade='all, delete-orphan')

class BoardGame(Base):
    __tablename__ = 'board_games'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship('User', back_populates='board_games')
    sessions = relationship('GameSession', back_populates='game')

class GameSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('board_games.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    deleted_players = Column(Boolean, default=False, server_default="false", nullable=False)

    game = relationship('BoardGame', back_populates='sessions')
    user = relationship('User', back_populates='sessions')
    session_players = relationship('SessionPlayer', back_populates='session', cascade='all, delete-orphan')


class SessionPlayer(Base):
    __tablename__ = 'session_player'
    session_id = Column(Integer, ForeignKey('sessions.id'), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    score = Column(Integer)
    winner = Column(Boolean, nullable=False)

    session = relationship('GameSession', back_populates='session_players')
    player = relationship('Player', back_populates='session_players')



