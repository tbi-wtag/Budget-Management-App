import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import category as category_crud
from app.crud import transaction as transaction_crud
from app.db.session import get_db
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)

router = APIRouter()


@router.get("", response_model=List[TransactionResponse], status_code=status.HTTP_200_OK)
async def list_transactions(db: AsyncSession = Depends(get_db)):
    return await transaction_crud.get_transactions(db)


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: TransactionCreate,
    db: AsyncSession = Depends(get_db),
):

    category = await category_crud.get_category_by_id(db, transaction_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category_id: Category does not exist",
        )
    return await transaction_crud.create_transaction(db, transaction_in)


@router.put("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
async def update_transaction(
    transaction_id: uuid.UUID,
    transaction_in: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
):

    db_transaction = await transaction_crud.get_transaction_by_id(db, transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    if transaction_in.category_id:
        category = await category_crud.get_category_by_id(db, transaction_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category_id: Category does not exist",
            )

    return await transaction_crud.update_transaction(db, db_transaction, transaction_in)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):

    db_transaction = await transaction_crud.get_transaction_by_id(db, transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    await transaction_crud.delete_transaction(db, db_transaction)
    return None