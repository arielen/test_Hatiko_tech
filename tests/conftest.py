import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app)
    ) as client:
        yield client
