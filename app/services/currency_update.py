import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session
from app.core.config import config
from app.applications.currency import (
    CurrencyController,
    CurrencyRateController,
)
from app.services.exc_rates_api import ExcRatesAPI


class CurrencyUpdate:

    @classmethod
    async def create_currencies(
        cls,
        session: AsyncSession,
    ):
        logging.info('No currencies found, trying to get them from API')
        currencies = await ExcRatesAPI.get_currencies()

        if not currencies:
            raise Exception('Can`t get currencies from API')

        for currency in currencies:
            await CurrencyController.create_or_update(
                origin=currency,
                session=session,
            )

        logging.info('Currencies created')

    @classmethod
    async def get_rates(
        cls,
        session: AsyncSession,
    ):
        rates = await ExcRatesAPI.get_rates()
        if not rates:
            raise Exception('Can`t get currency rates from API')

        for rate in rates:
            rate = await CurrencyRateController.create_or_update(
                session=session,
                origin=rate,
            )
            logging.info(
                f'Rate {rate.currency_left} -> {rate.currency_right} '
                f'update to {rate.rate}'
            )

    @classmethod
    async def run(cls) -> None:
        while True:
            async with async_session() as session:
                logging.info('Start updating currencies..')
                currencies = await CurrencyController.get_all(session=session)

                if not currencies:
                    await cls.create_currencies(session=session)

                await cls.get_rates(session=session)

                await asyncio.sleep(config.CURRENCY_UPDATE_STEP)