from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IMEI_SANDBOX_TOKEN: str
    # I didn't quite understand if the user passes the serviceId or not, 
    # so I had to take the one that is locked
    IMEI_SERVICE_ID: int

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
