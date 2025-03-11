from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from litestar.plugins.sqlalchemy import base


RoleEnum = SQLAlchemyEnum("Соискатель", "Работодатель", name="role_enum")


class Role(base.UUIDBase):
    __tablename__ = "roles"
    role_name: Mapped[str] = mapped_column(
        RoleEnum, nullable=False, unique=True, index=True
    )

