import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import base


class UserRole(base.UUIDAuditBase):
    __tablename__ = "user_roles"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship()
