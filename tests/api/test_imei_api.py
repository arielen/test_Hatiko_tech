from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from src.schemas.check import CheckCreate


@pytest.mark.anyio
async def test_check_imei_valid(async_client: AsyncClient):
    mock_response = CheckCreate(
        **{
            "id": "IagFtVaSUlpX9sPg",
            "type": "api",
            "status": "successful",
            "orderId": None,
            "service": {"id": 12, "title": "Mock service with only successful results"},
            "amount": "0.00",
            "deviceId": "860479069365109",
            "processedAt": 1738109120,
            "properties": {
                "deviceName": "iPhone SE (A2782)",
                "image": "https://sources.imeicheck.net/images/d8113afe344d275f6669d5cf955649c5.png",
                "serial": "0PNHCCLB26P",
                "estPurchaseDate": 1456293143,
            },
        }
    )
    with patch(
        "src.api.v1.endpoints.imei.check_imei",
        new=AsyncMock(return_value=mock_response),
    ):
        response = await async_client.post(
            "/v1/imei/check-imei",
            json={"imei": "860479069365109", "token": "fake_token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["deviceId"] == "860479069365109"
    assert data["properties"]["deviceName"] == "iPhone SE (A2782)"


@pytest.mark.anyio
async def test_check_imei_invalid(async_client: AsyncClient):
    with patch(
        "src.api.v1.endpoints.imei.check_imei",
        new=AsyncMock(return_value=None),
    ):
        response = await async_client.post(
            "/v1/imei/check-imei",
            json={"imei": "860479069365109", "token": "fake_token"},
        )
    assert response.status_code == 404
    assert response.json()["detail"] == "IMEI not found"


@pytest.mark.anyio
async def test_check_imei_error(async_client: AsyncClient):
    imei_invalid_short = "1234"
    response = await async_client.post(
        "/v1/imei/check-imei",
        json={"imei": imei_invalid_short, "token": "fake_token"},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, IMEI or S/N must be between 8 and 15 characters long"
    )

    imei_invalid_symbol = "!@#$%^&*()"
    response = await async_client.post(
        "/v1/imei/check-imei",
        json={"imei": imei_invalid_symbol, "token": "fake_token"},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, IMEI or S/N must contain only alphanumeric characters"
    )

    imei_invalid_luhn = "999999999999999"
    response = await async_client.post(
        "/v1/imei/check-imei",
        json={"imei": imei_invalid_luhn, "token": "fake_token"},
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, IMEI failed Luhn checksum validation"
    )
