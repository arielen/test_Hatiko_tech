import httpx
from fastapi import HTTPException

from src.core.config import settings
from src.schemas.check import CheckCreate
from src.schemas.imei import IMEIRequest

IMEI_CHECK_API_URL = "https://api.imeicheck.net/v1/checks"


async def check_imei(
    request: IMEIRequest,
    service_id: int = settings.IMEI_SERVICE_ID,
) -> CheckCreate | dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                IMEI_CHECK_API_URL,
                json={"deviceId": request.imei, "serviceId": service_id},
                headers={
                    "Authorization": f"Bearer {request.token or settings.IMEI_SANDBOX_TOKEN}",  # noqa: E501
                    "Accept-Language": "en",
                },
            )
            if response.status_code != 201:
                raise HTTPException(
                    status_code=response.status_code, detail="Something went wrong"
                )
            try:
                result: CheckCreate = CheckCreate(**response.json())
                return result
            except ValueError:
                raise HTTPException(status_code=404, detail="Device error IMEI")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Something went wrong")
