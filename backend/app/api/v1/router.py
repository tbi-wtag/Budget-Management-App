from fastapi import APIRouter

from app.api.v1 import categories, summary, transactions

api_router = APIRouter()

api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(summary.router, prefix="/summary", tags=["Summary"])