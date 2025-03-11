from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.cv import CV
from src.models.cv import CVCreate, CVResponse
from litestar.plugins.sqlalchemy import repository
from uuid import UUID
from msgspec import to_builtins


class CVRepository(repository.SQLAlchemyAsyncRepository[CV]):
    model_type = CV


async def provide_cv_repo(db_session: AsyncSession) -> CVRepository:
    return CVRepository(session=db_session)


class CVController(Controller):
    path = "/cvs"
    dependencies = {"cv_repo": Provide(provide_cv_repo)}

    @get("/")
    async def list_cvs(self, cv_repo: CVRepository) -> list[CVResponse]:
        results = await cv_repo.list()
        return [CVResponse(**to_builtins(cv)) for cv in results]

    @post("/")
    async def create_cv(self, data: CVCreate, cv_repo: CVRepository) -> CVResponse:
        cv = await cv_repo.add(CV(**to_builtins(data)))
        await cv_repo.session.commit()
        return CVResponse(**to_builtins(cv))

    @get("/{cv_id:uuid}")
    async def get_cv(self, cv_id: UUID, cv_repo: CVRepository) -> CVResponse:
        cv = await cv_repo.get(cv_id)
        return CVResponse(**to_builtins(cv))

    @delete("/{cv_id:uuid}")
    async def delete_cv(self, cv_id: UUID, cv_repo: CVRepository) -> None:
        await cv_repo.delete(cv_id)
        await cv_repo.session.commit()
