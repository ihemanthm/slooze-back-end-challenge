from pydantic import BaseModel
from datetime import datetime
from app.models.payment import PaymentMethodType


class PaymentMethodCreate(BaseModel):
    method_type: PaymentMethodType
    details: str
    is_default: bool = False


class PaymentMethodUpdate(BaseModel):
    details: str
    is_default: bool = False


class PaymentMethodResponse(BaseModel):
    id: int
    user_id: int
    method_type: PaymentMethodType
    details: str
    is_default: bool
    created_at: datetime

    class Config:
        from_attributes = True
