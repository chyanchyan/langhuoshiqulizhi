# coding: utf-8

from sqlalchemy import Integer, Column, Date, DateTime, \
    Float, ForeignKey, String, TEXT, func, BLOB, DECIMAL, DOUBLE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Players(Base):
    __tablename__ = "players"
    __table_args__ = {'schema': 'langhuo_db', 'comment': '玩家信息表'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)


class Games(Base):
    __tablename__ = "games"
    __table_args__ = {'schema': 'langhuo_db', 'comment': '牌局信息表'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    sb = Column(Integer, nullable=False)
    bb = Column(Integer, nullable=False)
    hands_count = Column(Integer, nullable=False)
    creator_id = Column(Integer, ForeignKey('langhuo_db.players.id'), nullable=False)



class GameRecords(Base):
    __tablename__ = "game_records"
    __table_args__ = {'schema': 'langhuo_db', 'comment': '牌局记录表'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    game_id = Column(Integer, ForeignKey('langhuo_db.games.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('langhuo_db.players.id'), nullable=False)
    hands_count = Column(Integer, nullable=False)
    buy_in_count = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)




