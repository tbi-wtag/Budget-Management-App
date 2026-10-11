import re

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import summary as summary_crud
from app.db.session import get_db
from app.schemas.summary import MonthlySummaryResponse

router = APIRouter()


@router.get("", response_model=MonthlySummaryResponse, status_code=status.HTTP_200_OK)
async def get_monthly_summary(
    month: str = Query(..., description="Target month in YYYY-MM format", examples=["2026-10"]),
    db: AsyncSession = Depends(get_db),
):
    if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", month):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid month format. Must be YYYY-MM (e.g. 2026-10)",
        )
    return await summary_crud.get_monthly_summary(db, month)