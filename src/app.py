from litestar import Litestar
from litestar.di import Provide
from src.controllers.user import UserController
from src.controllers.role import RoleController
from src.controllers.user_role import UserRoleController
from src.controllers.cv import CVController
from src.controllers.work_experience import WorkExperienceController
from src.controllers.company import CompanyController
from src.controllers.educational_institution import EducationalInstitutionController
from src.controllers.education import EducationController
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)
from litestar.openapi import OpenAPIConfig
from litestar.params import Parameter
from litestar.plugins.sqlalchemy import filters, base
from litestar.plugins.sqlalchemy import SQLAlchemySerializationPlugin


# Настройка базы данных
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/ltcats_test_db"


async def provide_limit_offset_pagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    ),
) -> filters.LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    current_page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return filters.LimitOffset(page_size, page_size * (current_page - 1))


session_config = AsyncSessionConfig(expire_on_commit=False)
db_config = SQLAlchemyAsyncConfig(
    connection_string=DATABASE_URL,
    before_send_handler="autocommit",
    session_config=session_config,
)


async def on_startup() -> None:
    """Initializes the database."""
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(base.UUIDBase.metadata.create_all)


sqlalchemy_plugin = SQLAlchemyInitPlugin(config=db_config)


app = Litestar(
    route_handlers=[
        UserController,
        RoleController,
        UserRoleController,
        CVController,
        WorkExperienceController,
        CompanyController,
        EducationalInstitutionController,
        EducationController,
    ],
    on_startup=[on_startup],
    openapi_config=OpenAPIConfig(title="My API", version="1.0.0"),
    dependencies={"limit_offset": Provide(provide_limit_offset_pagination)},
    plugins=[sqlalchemy_plugin, SQLAlchemySerializationPlugin()],
)
