from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException
from httpx import RequestError, Response

from src.schemas.check import CheckCreate
from src.schemas.imei import IMEIRequest
from src.services.imei_checker import check_imei


@pytest.mark.anyio
async def test_check_imei_success():
    mock_response_data = {
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

    with patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=Response(201, json=mock_response_data)),
    ):
        request = IMEIRequest(imei="860479069365109", token="fake_token")
        result = await check_imei(request)

        assert isinstance(result, CheckCreate)
        assert result.deviceId == mock_response_data["deviceId"]
        assert (
            result.properties.deviceName
            == mock_response_data["properties"]["deviceName"]
        )
        assert result.properties.image == mock_response_data["properties"]["image"]
        assert result.properties.serial == mock_response_data["properties"]["serial"]
        assert (
            result.properties.estPurchaseDate
            == mock_response_data["properties"]["estPurchaseDate"]
        )


@pytest.mark.anyio
async def test_check_imei_invalid_json():
    mock_response_data = {
        "id": "IagFtVaSUlpX9sPg",
        "type": "api",
        "nonvalid": "field",
        "meid": "86047906936510",
        "imei2": "056651627257128",
        "serial": "0PNHCCLB26P",
        "estPurchaseDate": 1456293143,
    }
    with patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=Response(201, json=mock_response_data)),
    ):
        request = IMEIRequest(imei="860479069365109", token="fake_token")
        with pytest.raises(HTTPException) as exc:
            await check_imei(request)

        assert exc.value.status_code == 404
        assert exc.value.detail == "Device error IMEI"


@pytest.mark.anyio
async def test_check_imei_http_error():
    with patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(return_value=Response(403, json={"error": "Forbidden"})),
    ):
        request = IMEIRequest(imei="860479069365109", token="fake_token")
        with pytest.raises(HTTPException) as exc:
            await check_imei(request)

        assert exc.value.status_code == 403
        assert exc.value.detail == "Something went wrong"


@pytest.mark.anyio
async def test_check_imei_request_error():
    with patch(
        "httpx.AsyncClient.post",
        new=AsyncMock(side_effect=RequestError("Network error")),
    ):
        request = IMEIRequest(imei="860479069365109", token="fake_token")
        with pytest.raises(HTTPException) as exc:
            await check_imei(request)

        assert exc.value.status_code == 500
        assert exc.value.detail == "Something went wrong"
