from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TELEGRAM_ADMIN_USERNAME: str
    TELEGRAM_ADMIN_ID: int
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_BOT_LINK: str
    NAME_PLATFORM: str
    SUPPORT_LINK: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    IMEI_SANDBOX_TOKEN: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
