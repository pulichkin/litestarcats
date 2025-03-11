from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.educational_institution import EducationalInstitution
from src.models.educational_institution import (
    EducationalInstitutionCreate,
    EducationalInstitutionResponse,
)
from litestar.plugins.sqlalchemy import repository
from uuid import UUID
from msgspec import to_builtins


class EducationalInstitutionRepository(
    repository.SQLAlchemyAsyncRepository[EducationalInstitution]
):
    model_type = EducationalInstitution


async def provide_institution_repo(
    db_session: AsyncSession,
) -> EducationalInstitutionRepository:
    return EducationalInstitutionRepository(session=db_session)


class EducationalInstitutionController(Controller):
    path = "/educational-institutions"
    dependencies = {"institution_repo": Provide(provide_institution_repo)}

    @get("/")
    async def list_institutions(
        self, institution_repo: EducationalInstitutionRepository
    ) -> list[EducationalInstitutionResponse]:
        results = await institution_repo.list()
        return [EducationalInstitutionResponse(**to_builtins(inst)) for inst in results]

    @post("/")
    async def create_institution(
        self,
        data: EducationalInstitutionCreate,
        institution_repo: EducationalInstitutionRepository,
    ) -> EducationalInstitutionResponse:
        inst = await institution_repo.add(EducationalInstitution(**to_builtins(data)))
        await institution_repo.session.commit()
        return EducationalInstitutionResponse(**to_builtins(inst))

    @get("/{inst_id:uuid}")
    async def get_institution(
        self, inst_id: UUID, institution_repo: EducationalInstitutionRepository
    ) -> EducationalInstitutionResponse:
        inst = await institution_repo.get(inst_id)
        return EducationalInstitutionResponse(**to_builtins(inst))

    @patch("/{inst_id:uuid}")
    async def update_institution(
        self,
        inst_id: UUID,
        data: EducationalInstitutionCreate,
        institution_repo: EducationalInstitutionRepository,
    ) -> EducationalInstitutionResponse:
        raw_obj = to_builtins(data, omit_none=True)
        raw_obj["id"] = inst_id
        inst = EducationalInstitution(**raw_obj)
        updated_inst = await institution_repo.update(inst)
        await institution_repo.session.commit()
        return EducationalInstitutionResponse(**to_builtins(updated_inst))

    @delete("/{inst_id:uuid}")
    async def delete_institution(
        self, inst_id: UUID, institution_repo: EducationalInstitutionRepository
    ) -> None:
        await institution_repo.delete(inst_id)
        await institution_repo.session.commit()
