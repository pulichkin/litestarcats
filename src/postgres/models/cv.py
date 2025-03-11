import uuid
from sqlalchemy import ForeignKey
from sqlalchemy import Index, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from litestar.plugins.sqlalchemy import base


class CV(base.UUIDAuditBase):
    __tablename__ = "cvs"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user: Mapped["User"] = relationship(back_populates="cvs")
    work_experiences: Mapped[list["WorkExperience"]] = relationship(back_populates="cv")
    educations: Mapped[list["Education"]] = relationship(back_populates="cv")
    __table_args__ = (Index("idx_cvs_created_at", "created_at"),)
