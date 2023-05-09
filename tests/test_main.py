import pytest

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.services.currency_update import CurrencyUpdate
from app.api import app
from app.core.config import config
from app.core.db import get_session, Base

from .request_mocks_data import (
    get_currencies_resp,
    get_rates_resp,
)


@pytest.fixture
def non_mocked_hosts() -> list:
    return ['testserver']


engine = create_async_engine(config.TEST_SQLLITE_URL, echo=False)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_test_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


app.dependency_overrides[get_session] = get_test_session
api_client = TestClient(app)


@pytest.mark.asyncio
async def test_main(
    httpx_mock,
) -> None:
    await create_tables()

    async with async_session() as session:
        httpx_mock.add_response(
            url=f'{config.EXCHANGERATES_API_URL}/symbols',
            json=get_currencies_resp,
        )
        await CurrencyUpdate.create_currencies(session=session)

        httpx_mock.add_response(
            url=f'{config.EXCHANGERATES_API_URL}/latest?base=USD',
            json=get_rates_resp,
        )
        await CurrencyUpdate.get_rates(session=session)

    resp = api_client.get('/rates')
    rates = resp.json()

    assert resp.status_code == 200
    assert rates['rates']['USD']['rate'] == 1
    assert rates['rates']['EUR']['rate'] == 0.910901
    assert rates['rates']['RUB']['rate'] == 77.40029

    resp = api_client.get(
        '/rates/convert',
        params={
            'convert_from': 'USD',
            'convert_to': 'RUB',
            'amount': 10,
        }
    )
    convert = resp.json()

    assert resp.status_code == 200
    assert convert['result'] == 77.40029


