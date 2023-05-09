from fastapi import APIRouter, Depends

from app.core.db import get_session
from app.schemas.rates import (
    CurrencyRateSchema,
    CurrencyRateListSchema,
    CurrencyConvertScheme,
)

from app.applications.currency import (
    CurrencyRateController,
)
from .exceptions import (
    rate_not_found,
    rates_not_found,
)


router = APIRouter(
    prefix='/rates',
    tags=['Курсы валют'],
)


@router.get(
    '/',
    response_model=CurrencyRateListSchema,
)
async def get_rates(
    session=Depends(get_session),
):
    rates = await CurrencyRateController.get_all(session=session)
    if not rates:
        raise rates_not_found()

    return CurrencyRateListSchema(rates={
        rate.currency_right: CurrencyRateSchema(
            currency_left=rate.currency_left,
            currency_right=rate.currency_right,
            rate=rate.rate,
            updated_at=rate.updated_at,
        ) for rate in rates
    })


@router.get(
    '/convert',
    response_model=CurrencyConvertScheme
)
async def convert(
    convert_from: str,
    convert_to: str,
    session=Depends(get_session),
):
    rate = await CurrencyRateController.get_by_currency(
        session=session,
        currency_left=convert_from,
        currency_right=convert_to,
    )

    return CurrencyConvertScheme(
        convert_from=convert_from,
        convert_to=convert_to,
        result=rate.rate,
    )


@router.get(
    '/{currency}',
    response_model=CurrencyRateSchema,
)
async def get_rate(
    currency: str,
    session=Depends(get_session),
):
    left_currency = 'EUR' if currency == 'USD' else 'USD'

    rate = await CurrencyRateController.get_by_currency(
        session=session,
        currency_left=left_currency,
        currency_right=currency,
    )

    if not rate:
        raise rate_not_found(code=currency)

    return CurrencyRateSchema(
        currency_left=rate.currency_left,
        currency_right=rate.currency_right,
        rate=rate.rate,
        updated_at=rate.updated_at,
    )
