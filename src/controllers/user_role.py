from litestar import Controller, get, post, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.user_role import UserRole
from src.models.user_role import UserRoleCreate, UserRoleResponse
from litestar.plugins.sqlalchemy import repository
from msgspec import to_builtins


class UserRoleRepository(repository.SQLAlchemyAsyncRepository[UserRole]):
    model_type = UserRole


async def provide_user_role_repo(db_session: AsyncSession) -> UserRoleRepository:
    return UserRoleRepository(session=db_session)


class UserRoleController(Controller):
    path = "/user-roles"
    dependencies = {"user_role_repo": Provide(provide_user_role_repo)}

    @get("/")
    async def list_user_roles(
        self, user_role_repo: UserRoleRepository
    ) -> list[UserRoleResponse]:
        results = await user_role_repo.list()
        return [UserRoleResponse(**to_builtins(ur)) for ur in results]

    @post("/")
    async def create_user_role(
        self, data: UserRoleCreate, user_role_repo: UserRoleRepository
    ) -> UserRoleResponse:
        ur = await user_role_repo.add(UserRole(**to_builtins(data)))
        await user_role_repo.session.commit()
        return UserRoleResponse(**to_builtins(ur))

    @delete("/{user_id:int}/{role_id:int}")
    async def delete_user_role(
        self, user_id: int, role_id: int, user_role_repo: UserRoleRepository
    ) -> None:
        await user_role_repo.delete((user_id, role_id))
        await user_role_repo.session.commit()
