from fastapi import APIRouter, HTTPException

from src.schemas.check import CheckCreate
from src.schemas.imei import IMEIRequest
from src.services.imei_checker import check_imei

router = APIRouter()


@router.post("/check-imei", description="Create Check")
async def check_imei_endpoint(request: IMEIRequest) -> CheckCreate:
    result = await check_imei(request=request, service_id=12)

    if result is None:
        raise HTTPException(status_code=404, detail="IMEI not found")

    return result
