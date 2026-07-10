from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile
    from app.models.manual_entry import ManualEntry


class User(Base, BaseModel):
    """
    Authentication model.
    Stores login credentials only.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    patient_profile: Mapped["PatientProfile"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    manual_entries: Mapped[list["ManualEntry"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )