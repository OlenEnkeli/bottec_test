from typing import List
from datetime import datetime as dt

from sqlalchemy import select, or_, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.currency import Currency, CurrencyRate
from app.schemas.rates import CurrencySchema, CurrencyRateSchema


class CurrencyController:

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> List[Currency]:
        query = (
            select(Currency)
            .order_by(Currency.code)
        )
        result = await session.scalars(query)
        return [c for c in result.all()]

    @classmethod
    async def get_by_code(
        cls,
        session: AsyncSession,
        code: str,
    ) -> Currency | None:
        query = (
            select(Currency)
            .filter(Currency.code == code)
        )

        fetch = await session.execute(query)
        return fetch.scalar_one_or_none()

    @classmethod
    async def create_or_update(
        cls,
        session: AsyncSession,
        origin: CurrencySchema,
    ) -> Currency | None:
        currency = Currency(
            code=origin.code,
            title=origin.title,
        )

        try:
            await session.merge(currency)
            await session.commit()
        except IntegrityError:
            return None

        return currency


class CurrencyRateController:
    @classmethod
    async def get_by_currency(
        cls,
        session: AsyncSession,
        currency_left: str,
        currency_right: str,
    ) -> CurrencyRate | None:
        query = (
            select(CurrencyRate)
            .filter(CurrencyRate.currency_left == currency_left)
            .filter(CurrencyRate.currency_right == currency_right)
        )

        fetch = await session.execute(query)
        rate = fetch.scalar_one_or_none()

        if rate:
            return rate

        query = (
            select(CurrencyRate)
            .filter(CurrencyRate.currency_left == currency_right)
            .filter(CurrencyRate.currency_right == currency_left)
        )

        fetch = await session.execute(query)
        rate = fetch.scalar_one_or_none()

        if rate:
            return CurrencyRate(
                currency_left=currency_left,
                currency_right=currency_right,
                rate=(1/rate.rate)
            )

        query_from = (
            select(CurrencyRate)
            .filter(CurrencyRate.currency_left == 'USD')
            .filter(CurrencyRate.currency_right == currency_left)
        )

        query_to = (
            select(CurrencyRate)
            .filter(CurrencyRate.currency_left == 'USD')
            .filter(CurrencyRate.currency_right == currency_right)
        )

        fetch_from = await session.execute(query_from)
        fetch_to = await session.execute(query_to)

        rate_from = fetch_from.scalar_one_or_none()
        rate_to = fetch_to.scalar_one_or_none()

        return CurrencyRate(
            currency_left=currency_left,
            currency_right=currency_right,
            rate=(rate_to.rate / rate_from.rate),
        )

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> List[CurrencyRate]:
        query = (
            select(CurrencyRate)
            .order_by(CurrencyRate.currency_right)
        )

        fetch = await session.execute(query)
        return fetch.scalars()

    @classmethod
    async def create_or_update(
        cls,
        session: AsyncSession,
        origin: CurrencyRateSchema,
    ) -> CurrencyRate | None:
        rate = CurrencyRate(
            currency_left=origin.currency_left,
            currency_right=origin.currency_right,
            rate=origin.rate,
            updated_at=dt.now()
        )

        try:
            await session.merge(rate)
            await session.commit()
        except IntegrityError:
            return None

        return rate
