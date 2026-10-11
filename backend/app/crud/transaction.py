import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

async def get_transactions(db: AsyncSession) -> List[Transaction]:
    statement = (
        select(Transaction)
        .options(selectinload(Transaction.category))
        .order_by(Transaction.created_at.desc())
    )
    result = await db.execute(statement)
    return list(result.scalars().all())

async def get_transaction_by_id(
    db: AsyncSession, transaction_id: uuid.UUID) -> Optional[Transaction]:
    statement = (
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.id == transaction_id)
    )
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def create_transaction(
    db: AsyncSession, transaction_in: TransactionCreate) -> Transaction:
    db_transaction = Transaction(
        amount=transaction_in.amount,
        description=transaction_in.description,
        type=transaction_in.type,
        category_id=transaction_in.category_id,
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return await get_transaction_by_id(db, db_transaction.id)

async def update_transaction(
    db: AsyncSession,
    db_transaction: Transaction,
    transaction_in: TransactionUpdate,) -> Transaction:
    update_data = transaction_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    await db.commit()
    await db.refresh(db_transaction)
    return await get_transaction_by_id(db, db_transaction.id)

async def delete_transaction(
    db: AsyncSession, db_transaction: Transaction) -> None:
    await db.delete(db_transaction)
    await db.commit()