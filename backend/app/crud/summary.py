from typing import List

from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category, TransactionType
from app.models.transaction import Transaction
from app.schemas.summary import CategoryExpenseSummary, MonthlySummaryResponse


async def get_monthly_summary(
    db: AsyncSession, month_str: str) -> MonthlySummaryResponse:
    year, month = map(int, month_str.split("-"))

    # 1. Total Income
    income_stmt = select(func.coalesce(func.sum(Transaction.amount), 0.0)).where(
        Transaction.type == TransactionType.INCOME,
        extract("year", Transaction.created_at) == year,
        extract("month", Transaction.created_at) == month,
    )
    income_result = await db.execute(income_stmt)
    total_income = float(income_result.scalar_one())

    # 2. Total Expenses
    expense_stmt = select(func.coalesce(func.sum(Transaction.amount), 0.0)).where(
        Transaction.type == TransactionType.EXPENSE,
        extract("year", Transaction.created_at) == year,
        extract("month", Transaction.created_at) == month,
    )
    expense_result = await db.execute(expense_stmt)
    total_expenses = float(expense_result.scalar_one())

    # 3. Net Balance
    balance = total_income - total_expenses

    # 4. Group Expenses by Category
    category_stmt = (
        select(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.coalesce(func.sum(Transaction.amount), 0.0).label("total_amount"),
        )
        .join(Transaction, Category.id == Transaction.category_id)
        .where(
            Transaction.type == TransactionType.EXPENSE,
            extract("year", Transaction.created_at) == year,
            extract("month", Transaction.created_at) == month,
        )
        .group_by(Category.id, Category.name)
    )
    category_results = await db.execute(category_stmt)

    expenses_by_category: List[CategoryExpenseSummary] = [
        CategoryExpenseSummary(
            category_id=row.category_id,
            category_name=row.category_name,
            total_amount=float(row.total_amount),
        )
        for row in category_results.all()
    ]

    return MonthlySummaryResponse(
        month=month_str,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        expenses_by_category=expenses_by_category,
    )