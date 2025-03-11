from sqlalchemy import String
from sqlalchemy import CheckConstraint, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import base
from typing import Optional


InstitutionTypeEnum = SQLAlchemyEnum(
    "Университет",
    "Институт",
    "Колледж",
    "Школа",
    "Курс",
    name="institution_type_enum"
)


class EducationalInstitution(base.UUIDAuditBase):
    __tablename__ = "educational_institutions"
    institution_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    institution_type: Mapped[str] = mapped_column(
        InstitutionTypeEnum, nullable=False, index=True
    )
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(255))
    accreditation: Mapped[Optional[str]] = mapped_column(String(100))
    educations: Mapped[list["Education"]] = relationship(back_populates="institution")
    __table_args__ = (
        CheckConstraint(
            "length(institution_name) > 0", name="check_institution_name_not_empty"
        ),
        CheckConstraint("length(location) > 0", name="check_location_not_empty"),
    )
