from fastapi import APIRouter

from .endpoints import imei

__version__ = "0.0.1"

router = APIRouter()

router.include_router(imei.router, prefix="/imei", tags=["IMEI"])
