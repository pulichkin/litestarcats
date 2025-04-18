import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy import CheckConstraint, Index, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from litestar.plugins.sqlalchemy import base


EmploymentTypeEnum = SQLAlchemyEnum(
    "Полная занятость",
    "Частичная занятость",
    "Удаленная работа",
    name="employment_type_enum",
)


class WorkExperience(base.UUIDAuditBase):
    __tablename__ = "work_experience"
    cv_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    employment_type: Mapped[str] = mapped_column(
        EmploymentTypeEnum, nullable=False, index=True
    )
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    cv: Mapped["CV"] = relationship(back_populates="work_experiences")
    company: Mapped["Company"] = relationship(back_populates="work_experiences")
    __table_args__ = (
        CheckConstraint("length(job_title) > 0", name="check_job_title_not_empty"),
        CheckConstraint(
            "start_date <= end_date OR end_date IS NULL", name="check_date_order"
        ),
        Index("idx_work_exp_dates", "start_date", "end_date"),
    )
