from litestar import Controller, get, post, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.role import Role
from src.models.role import RoleCreate, RoleResponse
from litestar.plugins.sqlalchemy import repository
from uuid import UUID
from msgspec import to_builtins


class RoleRepository(repository.SQLAlchemyAsyncRepository[Role]):
    model_type = Role


async def provide_role_repo(db_session: AsyncSession) -> RoleRepository:
    return RoleRepository(session=db_session)


class RoleController(Controller):
    path = "/roles"
    dependencies = {"role_repo": Provide(provide_role_repo)}

    @get("/")
    async def list_roles(self, role_repo: RoleRepository) -> list[RoleResponse]:
        results = await role_repo.list()
        return [RoleResponse(**to_builtins(role)) for role in results]

    @post("/")
    async def create_role(
        self, data: RoleCreate, role_repo: RoleRepository
    ) -> RoleResponse:
        role = await role_repo.add(Role(**to_builtins(data)))
        await role_repo.session.commit()
        return RoleResponse(**to_builtins(role))

    @get("/{role_id:uuid}")
    async def get_role(self, role_id: UUID, role_repo: RoleRepository) -> RoleResponse:
        role = await role_repo.get(role_id)
        return RoleResponse(**to_builtins(role))

    @delete("/{role_id:uuid}")
    async def delete_role(self, role_id: UUID, role_repo: RoleRepository) -> None:
        await role_repo.delete(role_id)
        await role_repo.session.commit()
