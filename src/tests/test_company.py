import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.company import CompanyCreate
from src.postgres.models.company import Company
from sqlalchemy import select
from msgspec import structs


# Тесты для Company
@pytest.mark.asyncio
async def test_create_company(db_session: AsyncSession):
    company_data = CompanyCreate(
        company_name="New LtCats Corp",
        industry="Tech",
    )
    company = Company(**structs.asdict(company_data))

    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)

    result = await db_session.get(Company, company.id)
    assert result.company_name == company.company_name
    assert result.industry == company.industry
