from sqlalchemy import String
from sqlalchemy import CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import base
from typing import Optional


class User(base.UUIDAuditBase):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    profile_photo_url: Mapped[Optional[str]] = mapped_column(String(255))
    user_roles: Mapped[list["UserRole"]] = relationship(back_populates="user")
    cvs: Mapped[list["CV"]] = relationship(back_populates="user")
    __table_args__ = (
        CheckConstraint("length(first_name) > 0", name="check_first_name_not_empty"),
        CheckConstraint("length(last_name) > 0", name="check_last_name_not_empty"),
        CheckConstraint("email LIKE '%@%.%'", name="check_email_format"),
        Index("idx_users_created_at", "created_at"),
    )
