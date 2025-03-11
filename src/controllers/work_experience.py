from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.work_experience import WorkExperience
from src.models.work_experience import WorkExperienceCreate, WorkExperienceResponse
from litestar.plugins.sqlalchemy import repository
from uuid import UUID
from msgspec import to_builtins


class WorkExperienceRepository(repository.SQLAlchemyAsyncRepository[WorkExperience]):
    model_type = WorkExperience


async def provide_work_experience_repo(
    db_session: AsyncSession,
) -> WorkExperienceRepository:
    return WorkExperienceRepository(session=db_session)


class WorkExperienceController(Controller):
    path = "/work-experiences"
    dependencies = {"work_experience_repo": Provide(provide_work_experience_repo)}

    @get("/")
    async def list_work_experiences(
        self, work_experience_repo: WorkExperienceRepository
    ) -> list[WorkExperienceResponse]:
        results = await work_experience_repo.list()
        return [WorkExperienceResponse(**to_builtins(we)) for we in results]

    @post("/")
    async def create_work_experience(
        self, data: WorkExperienceCreate, work_experience_repo: WorkExperienceRepository
    ) -> WorkExperienceResponse:
        we = await work_experience_repo.add(WorkExperience(**to_builtins(data)))
        await work_experience_repo.session.commit()
        return WorkExperienceResponse(**to_builtins(we))

    @get("/{we_id:uuid}")
    async def get_work_experience(
        self, we_id: UUID, work_experience_repo: WorkExperienceRepository
    ) -> WorkExperienceResponse:
        we = await work_experience_repo.get(we_id)
        return WorkExperienceResponse(**to_builtins(we))

    @patch("/{we_id:uuid}")
    async def update_work_experience(
        self,
        we_id: UUID,
        data: WorkExperienceCreate,
        work_experience_repo: WorkExperienceRepository,
    ) -> WorkExperienceResponse:
        raw_obj = to_builtins(data, omit_none=True)
        raw_obj["id"] = we_id
        we = WorkExperience(**raw_obj)
        updated_we = await work_experience_repo.update(we)
        await work_experience_repo.session.commit()
        return WorkExperienceResponse(**to_builtins(updated_we))

    @delete("/{we_id:uuid}")
    async def delete_work_experience(
        self, we_id: UUID, work_experience_repo: WorkExperienceRepository
    ) -> None:
        await work_experience_repo.delete(we_id)
        await work_experience_repo.session.commit()
