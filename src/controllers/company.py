from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.postgres.models.company import Company
from src.models.company import CompanyCreate, CompanyResponse
from litestar.plugins.sqlalchemy import repository
from uuid import UUID
from msgspec import to_builtins


class CompanyRepository(repository.SQLAlchemyAsyncRepository[Company]):
    model_type = Company


async def provide_company_repo(db_session: AsyncSession) -> CompanyRepository:
    return CompanyRepository(session=db_session)


class CompanyController(Controller):
    path = "/companies"
    dependencies = {"company_repo": Provide(provide_company_repo)}

    @get("/")
    async def list_companies(
        self, company_repo: CompanyRepository
    ) -> list[CompanyResponse]:
        results = await company_repo.list()
        return [CompanyResponse(**to_builtins(company)) for company in results]

    @post("/")
    async def create_company(
        self, data: CompanyCreate, company_repo: CompanyRepository
    ) -> CompanyResponse:
        company = await company_repo.add(Company(**to_builtins(data)))
        await company_repo.session.commit()
        return CompanyResponse(**to_builtins(company))

    @get("/{company_id:uuid}")
    async def get_company(
        self, company_id: UUID, company_repo: CompanyRepository
    ) -> CompanyResponse:
        company = await company_repo.get(company_id)
        return CompanyResponse(**to_builtins(company))

    @patch("/{company_id:uuid}")
    async def update_company(
        self, company_id: UUID, data: CompanyCreate, company_repo: CompanyRepository
    ) -> CompanyResponse:
        raw_obj = to_builtins(data, omit_none=True)
        raw_obj["id"] = company_id
        company = Company(**raw_obj)
        updated_company = await company_repo.update(company)
        await company_repo.session.commit()
        return CompanyResponse(**to_builtins(updated_company))

    @delete("/{company_id:uuid}")
    async def delete_company(
        self, company_id: UUID, company_repo: CompanyRepository
    ) -> None:
        await company_repo.delete(company_id)
        await company_repo.session.commit()
