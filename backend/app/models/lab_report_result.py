from __future__ import annotations
import uuid
from sqlalchemy import UUID
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel
from app.common.enums import LabResultStatus

if TYPE_CHECKING:
    from app.models.lab_report import LabReport


class LabReportResult(Base, BaseModel):
    __tablename__ = "lab_report_results"

    lab_report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lab_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parameter_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    parameter_value: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    reference_range: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[LabResultStatus] = mapped_column(
        Enum(LabResultStatus),
        nullable=False,
    )

    lab_report: Mapped["LabReport"] = relationship(
        back_populates="results"
    )