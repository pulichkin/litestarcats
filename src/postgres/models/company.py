from sqlalchemy import String
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import base
from typing import Optional


class Company(base.UUIDAuditBase):
    __tablename__ = "companies"
    logo_url: Mapped[Optional[str]] = mapped_column(String(255))
    company_name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255))
    work_experiences: Mapped[list["WorkExperience"]] = relationship(
        back_populates="company"
    )
    __table_args__ = (
        CheckConstraint(
            "length(company_name) > 0", name="check_company_name_not_empty"
        ),
        CheckConstraint("length(industry) > 0", name="check_industry_not_empty"),
    )
