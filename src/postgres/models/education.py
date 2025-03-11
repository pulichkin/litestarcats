import uuid
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import base
from typing import Optional


class Education(base.UUIDBase):
    __tablename__ = "education"
    cv_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cvs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("educational_institutions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    degree: Mapped[str] = mapped_column(String(100), nullable=False)
    field_of_study: Mapped[str] = mapped_column(String(100), nullable=False)
    start_year: Mapped[int] = mapped_column(nullable=False)
    end_year: Mapped[Optional[int]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    cv: Mapped["CV"] = relationship(back_populates="educations")
    institution: Mapped["EducationalInstitution"] = relationship(
        back_populates="educations"
    )
    __table_args__ = (
        CheckConstraint("length(degree) > 0", name="check_degree_not_empty"),
        CheckConstraint(
            "length(field_of_study) > 0", name="check_field_of_study_not_empty"
        ),
        CheckConstraint(
            "start_year <= end_year OR end_year IS NULL", name="check_year_order"
        ),
    )
