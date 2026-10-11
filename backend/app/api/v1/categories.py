import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import category as category_crud
from app.db.session import get_db
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()


@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def list_categories(db: AsyncSession = Depends(get_db)):
    return await category_crud.get_categories(db)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await category_crud.create_category(db, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    db_category = await category_crud.get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    await category_crud.delete_category(db, db_category)
    return None