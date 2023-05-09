from datetime import datetime as dt
from typing import List, Dict

from pydantic import BaseModel


class CurrencySchema(BaseModel):
    code: str
    title: str


class CurrencyRateSchema(BaseModel):
    currency_left: str
    currency_right: str
    rate: float
    updated_at: dt | None


class CurrencyListSchema(BaseModel):
    currencies: List[CurrencySchema]


class CurrencyRateListSchema(BaseModel):
    rates: Dict[str, CurrencyRateSchema]


class CurrencyConvertScheme(BaseModel):
    convert_from: str
    convert_to: str
    result: float
