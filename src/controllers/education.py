from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.education import Education
from src.models.education import EducationCreate, EducationResponse
from litestar.plugins.sqlalchemy import repository
from uuid import UUID
from msgspec import to_builtins


class EducationRepository(repository.SQLAlchemyAsyncRepository[Education]):
    model_type = Education


async def provide_education_repo(db_session: AsyncSession) -> EducationRepository:
    return EducationRepository(session=db_session)


class EducationController(Controller):
    path = "/educations"
    dependencies = {"education_repo": Provide(provide_education_repo)}

    @get("/")
    async def list_educations(
        self, education_repo: EducationRepository
    ) -> list[EducationResponse]:
        results = await education_repo.list()
        return [EducationResponse(**to_builtins(edu)) for edu in results]

    @post("/")
    async def create_education(
        self, data: EducationCreate, education_repo: EducationRepository
    ) -> EducationResponse:
        edu = await education_repo.add(Education(**to_builtins(data)))
        await education_repo.session.commit()
        return EducationResponse(**to_builtins(edu))

    @get("/{edu_id:uuid}")
    async def get_education(
        self, edu_id: UUID, education_repo: EducationRepository
    ) -> EducationResponse:
        edu = await education_repo.get(edu_id)
        return EducationResponse(**to_builtins(edu))

    @patch("/{edu_id:uuid}")
    async def update_education(
        self, edu_id: UUID, data: EducationCreate, education_repo: EducationRepository
    ) -> EducationResponse:
        raw_obj = to_builtins(data, omit_none=True)
        raw_obj["id"] = edu_id
        edu = Education(**raw_obj)
        updated_edu = await education_repo.update(edu)
        await education_repo.session.commit()
        return EducationResponse(**to_builtins(updated_edu))

    @delete("/{edu_id:uuid}")
    async def delete_education(
        self, edu_id: UUID, education_repo: EducationRepository
    ) -> None:
        await education_repo.delete(edu_id)
        await education_repo.session.commit()
