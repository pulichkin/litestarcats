from litestar import Litestar
from litestar.di import Provide
from src.controllers.user import UserController, provide_users_repo
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
from litestar.connection import ASGIConnection
from litestar.openapi import OpenAPIConfig
from litestar.params import Parameter
from litestar.plugins.sqlalchemy import filters, base
from litestar.plugins.sqlalchemy import SQLAlchemySerializationPlugin
from litestar.security.jwt import JWTAuth, Token
from litestar.logging import LoggingConfig
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from uuid import UUID
from src.configs.app_config import configure
from src.postgres.models.user import User
from jinja2 import Environment, PackageLoader, select_autoescape


# Загружаем конфиги
config = configure()

logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["queue_listener"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    log_exceptions="always",  # Включить логирование исключений с трассировкой
)

env = Environment(
        loader=PackageLoader("src"),
        autoescape=select_autoescape()
        )


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


sessionmaker = async_sessionmaker(expire_on_commit=False)


async def retrieve_user_handler(
    token: Token,
    connection: ASGIConnection,
) -> User | None:
    user_id = UUID(token.sub)
    users_repo = connection.scope.get("users_repo")
    if not users_repo:
        async with sessionmaker(bind=db_config.get_engine()) as session:
            try:
                async with session.begin():
                    users_repo = await provide_users_repo(db_session=session)
            except IntegrityError as exc:
                raise ClientException(
                    status_code=HTTP_409_CONFLICT,
                    detail=str(exc),
                ) from exc
    user = await users_repo.get(user_id)
    return user


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=config.jwt.token_secret,
    algorithm="HS256",
    exclude=["/users", "/schema"]
)


session_config = AsyncSessionConfig(expire_on_commit=False)
db_config = SQLAlchemyAsyncConfig(
    connection_string=config.database.get_connection_url(),
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
    on_app_init=[jwt_auth.on_app_init],
    openapi_config=OpenAPIConfig(title="My API", version="1.0.0"),
    dependencies={
        "limit_offset": Provide(provide_limit_offset_pagination),
        },
    plugins=[sqlalchemy_plugin, SQLAlchemySerializationPlugin()],
    logging_config=logging_config,
)
