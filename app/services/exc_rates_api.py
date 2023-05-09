import logging

from typing import List

from httpx import AsyncClient

from app.core.retry import api_retry
from app.core.config import config
from app.schemas.exc_rates_api import (
    ExcRatesCurrencyListSchema,
    ExcRatesRateListSchema,
)
from app.schemas.rates import (
    CurrencySchema,
    CurrencyRateSchema,
)


class ExcRatesException(Exception):
    def __init__(self, error: str):
        self.error = error

    def __str__(self):
        return f'ExcRates: {self.error}'


class ExcRatesAPI:
    @classmethod
    @api_retry
    async def get_currencies(cls) -> List[CurrencySchema]:
        async with AsyncClient() as client:
            resp = await client.get(
                url=f'{config.EXCHANGERATES_API_URL}/symbols',
                headers={'apikey': config.EXCHANGERATES_API_KEY}
            )
            if resp.status_code not in (200, 201):
                raise ExcRatesException(
                    f'Can`t get currencies - non 20* code\n'
                    f'{resp.request.url} - {resp.status_code}'
                )
            parsed = ExcRatesCurrencyListSchema.parse_obj(resp.json())

            if not parsed.success:
                raise ExcRatesException('Can`t get currencies - success=false')

            return [
                CurrencySchema(
                    code=currency.code,
                    title=currency.title,
                ) for currency in parsed.symbols
            ]

    @classmethod
    @api_retry
    async def get_rates(cls) -> List[CurrencyRateSchema] | None:
        async with AsyncClient() as client:
            resp = await client.get(
                url=f'{config.EXCHANGERATES_API_URL}/latest',
                headers={'apikey': config.EXCHANGERATES_API_KEY},
                params={'base': 'USD'},
                timeout=5,
            )
            if resp.status_code not in (200, 201):
                raise ExcRatesException('Can`t get rates - non 20* code')
            print(resp.text)
            parsed = ExcRatesRateListSchema.parse_obj(resp.json())

            if not parsed.success:
                raise ExcRatesException('Can`t get currencies - success=false')

            return [
                CurrencyRateSchema(
                    currency_left='USD',
                    currency_right=rate.code,
                    rate=rate.value,
                ) for rate in parsed.rates
            ]