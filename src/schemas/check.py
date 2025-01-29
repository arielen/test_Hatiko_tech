from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class Status(str, Enum):
    SUCCESSFUL = "successful"
    UNSUCCESSFUL = "unsuccessful"
    FAILED = "failed"


class Service(BaseModel):
    id: int
    title: str


class Property(BaseModel):
    deviceName: str
    image: str
    serial: str
    estPurchaseDate: int
    additional_data: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data):
        known_fields = {
            "deviceName",
            "image",
            "serial",
            "estPurchaseDate",
        }
        additional_data = {k: v for k, v in data.items() if k not in known_fields}
        super().__init__(**data, additional_data=additional_data)


class CheckCreate(BaseModel):
    id: str
    type: str = Field(default="api")
    status: Status
    orderId: Optional[str]
    service: Service
    amount: str
    deviceId: str
    processedAt: int
    properties: Union[Property, List]
