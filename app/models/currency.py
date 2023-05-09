import asyncio

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)

from app.core.db import Base


class Currency(Base):
    __tablename__ = 'currency'

    code = Column(String, primary_key=True, index=True)
    title = Column(String)


class CurrencyRate(Base):
    __tablename__ = 'currency_rate'
    __table_args__ = (
        PrimaryKeyConstraint('currency_left', 'currency_right'),
    )

    currency_left = Column(String, ForeignKey('currency.code'))
    currency_right = Column(String, ForeignKey('currency.code'))
    rate = Column(Float)
    updated_at = Column(DateTime)
