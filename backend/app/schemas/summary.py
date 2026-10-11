import uuid
from typing import List

from pydantic import BaseModel, Field

class CategoryExpenseSummary(BaseModel):
    category_id: uuid.UUID
    category_name: str
    total_amount: float = Field(..., ge=0)

class MonthlySummaryResponse(BaseModel):
    month: str = Field(..., examples=["2026-10"])
    total_income: float = Field(..., ge=0)
    total_expenses: float = Field(..., ge=0)
    balance: float
    expenses_by_category: List[CategoryExpenseSummary]