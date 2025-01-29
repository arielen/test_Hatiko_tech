import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_check_imei_valid(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the IMEI Checker API"
