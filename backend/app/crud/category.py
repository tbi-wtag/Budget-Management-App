import uuid 
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate

async def get_categories(db: AsyncSession) -> List[Category]:
    statement = select(Category).order_by(Category.name.asc())
    result = await db.execute(statement)
    return list(result.scalars().all())

async def get_category_by_id(
    db: AsyncSession, category_id: uuid.UUID) -> Optional[Category]:
    statement = select(Category).where(Category.id == category_id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

async def create_category(
    db: AsyncSession, category_in: CategoryCreate) -> Category:
    db_category = Category(
        name=category_in.name,
        type=category_in.type,
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def delete_category(
    db: AsyncSession, db_category: Category) -> None:
    await db.delete(db_category)
    await db.commit()