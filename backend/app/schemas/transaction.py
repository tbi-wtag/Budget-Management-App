import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.category import TransactionType

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, examples=[45.50])
    description: str = Field(None, max_length=255, examples=["Grocery shopping"])
    type: TransactionType = Field(..., examples=[TransactionType.EXPENSE])

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    amount: Optional[float] = Field(None, gt=0, examples=[50.00])
    description: Optional[str] = Field(None, max_length=255, examples=["Updated description"])
    type: Optional[TransactionType] = None
    category_id: Optional[uuid.UUID] = None

class TransactionResponse(TransactionBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)