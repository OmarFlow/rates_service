#!/usr/bin/env python3
from __future__ import annotations
import datetime
from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import func, UniqueConstraint


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Symbol(Base):
    __tablename__ = "symbol"
    __table_args__ = (UniqueConstraint("name"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    history: Mapped[List[SymbolHistory]] = relationship("SymbolHistory")

    def __repr__(self):
        return f"Symbol_{self.name} with id_{self.id}"


class SymbolHistory(Base):
    __tablename__ = "symbol_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    symbol_id = mapped_column(ForeignKey("symbol.id"))
    exchanger: Mapped[str] = mapped_column(server_default="binance")
    value: Mapped[str]

