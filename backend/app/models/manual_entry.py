from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class ManualEntry(Base,BaseModel):
    __tablename__ = "manual_entries"

   

    user_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
)

    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)

    metric_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    unit: Mapped[str | None] = mapped_column(String(30), nullable=True)

    category: Mapped[str] = mapped_column(String(50), nullable=False)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    recorded_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    
    user: Mapped["User"] = relationship(
    back_populates="manual_entries"
)