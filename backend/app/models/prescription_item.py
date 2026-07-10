from __future__ import annotations

from typing import TYPE_CHECKING
import uuid
from sqlalchemy import Boolean, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.medication import Medication
    from app.models.prescription import Prescription


class PrescriptionItem(Base, BaseModel):
    __tablename__ = "prescription_items"

    prescription_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prescriptions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    medication_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("medications.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    duration_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    morning: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    afternoon: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    evening: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    night: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    before_food: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    after_food: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    prescription: Mapped["Prescription"] = relationship(
        back_populates="items"
    )

    medication: Mapped["Medication"] = relationship(
        back_populates="prescription_items"
    )