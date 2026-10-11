import enum
from typing import TYPE_CHECKING, List

from sqlalchemy import Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampedUUIDMixin

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Category(Base, TimestampedUUIDMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)


    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType), nullable=False
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="category",
        cascade="all, delete-orphan",
    )