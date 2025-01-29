from src.core.config import settings


def test_config():
    assert settings.IMEI_SANDBOX_TOKEN is not None
    assert settings.IMEI_SERVICE_ID is not None
