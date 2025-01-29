from fastapi import FastAPI

from src.api.v1 import router as router_v1

app = FastAPI(
    title="IMEI Checker", description="API for checking IMEI numbers", version="0.0.1"
)

app.include_router(router_v1, prefix="/v1", tags=["API v1"])


@app.get("/")
async def root():
    return {"message": "Welcome to the IMEI Checker API"}
