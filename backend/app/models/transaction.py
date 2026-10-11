import uuid
from typing import Optional

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampedUUIDMixin
from app.models.category import Category, TransactionType

class Transaction(Base,TimestampedUUIDMixin):
    __tablename__ = "transactions"

    amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )

    category: Mapped["Category"] = relationship("Category", back_populates="transactions")

