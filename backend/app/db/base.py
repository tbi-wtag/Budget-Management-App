import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class TimestampedUUIDMixin:

    id: Mapped[uuid:UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        server_default=text("now()"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        server_default=text("now()"),
    )
    