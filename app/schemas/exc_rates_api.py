from typing import List

from pydantic import BaseModel, validator


class ExcRatesBaseSchema(BaseModel):
    success: bool


class ExcRatesCurrencySchema(BaseModel):
    code: str
    title: str


class ExcRatesCurrencyListSchema(ExcRatesBaseSchema):
    symbols: List[ExcRatesCurrencySchema]

    @validator('symbols', pre=True)
    def validate_symbols(cls, v: dict):
        return [
            ExcRatesCurrencySchema(
                code=key,
                title=value,
            ) for key, value in v.items()
        ]


class ExcRatesRateSchema(BaseModel):
    code: str | None
    value: float | None


class ExcRatesRateListSchema(ExcRatesBaseSchema):
    rates: List[ExcRatesRateSchema]
    base: str
    timestamp: int

    @validator('rates', pre=True)
    def validate_symbols(cls, v: dict):
        return [
            ExcRatesRateSchema(
                code=key,
                value=value,
            ) for key, value in v.items()
        ]
