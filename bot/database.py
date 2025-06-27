from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

import pandas as pd
from sqlalchemy import JSON, Column, DateTime, Integer, Numeric, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    side = Column(String(10))
    status = Column(String(20))
    entry_price = Column(Numeric)
    stop_loss = Column(Numeric)
    take_profit = Column(Numeric)
    indicators = Column(JSONB)
    created_at = Column(DateTime)
    closed_at = Column(DateTime)


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    price = Column(Numeric)
    quantity = Column(Numeric)
    created_at = Column(DateTime)


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(20))
    side = Column(String(10))
    quantity = Column(Numeric)
    entry_price = Column(Numeric)
    stop_loss = Column(Numeric)
    take_profit = Column(Numeric)
    created_at = Column(DateTime)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    level = Column(String(10))
    message = Column(String)
    created_at = Column(DateTime)


class Database:
    """Database helper class for PostgreSQL."""

    def __init__(self, uri: str) -> None:
        self.engine = create_engine(uri)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(self.__class__.__name__)

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def insert_order(self, data: Dict[str, Any]) -> int:
        session = self.SessionLocal()
        try:
            order = Order(**data)
            session.add(order)
            session.commit()
            session.refresh(order)
            return order.id
        finally:
            session.close()

    def insert_trade(self, data: Dict[str, Any]) -> int:
        session = self.SessionLocal()
        try:
            trade = Trade(**data)
            session.add(trade)
            session.commit()
            session.refresh(trade)
            return trade.id
        finally:
            session.close()

    # Additional database methods would go here (update positions, logs, etc.)
