import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.category import TransactionType

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100, examples=["Food","Transport", "Salary"])
    type: TransactionType = Field(..., examples=[TransactionType.EXPENSE])

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)