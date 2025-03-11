import pytest
from datetime import datetime, timezone
from src.postgres.models.company import Company
from src.postgres.models.cv import CV
from src.postgres.models.work_experience import WorkExperience
from sqlalchemy import select
from sqlalchemy.orm import joinedload


# Тесты для WorkExperience
@pytest.mark.asyncio
async def test_create_work_experience(db_session, test_cv, test_company):
    work_exp = WorkExperience(
        cv_id=test_cv.id,
        company_id=test_company.id,
        job_title="Мурлыкатель",
        employment_type="Полная занятость",
        start_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
    )
    db_session.add(work_exp)
    await db_session.commit()

    result = await db_session.get(WorkExperience, work_exp.id)
    assert result.job_title == "Мурлыкатель"
    assert result.cv_id == test_cv.id
    assert result.company_id == test_company.id


@pytest.mark.asyncio
async def test_work_experience_relationship(db_session, test_cv, test_company):
    work_exp = WorkExperience(
        cv_id=test_cv.id,
        company_id=test_company.id,
        job_title="Фырчатель",
        employment_type="Полная занятость",
        start_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
    )
    db_session.add(work_exp)
    await db_session.commit()
    await db_session.refresh(work_exp)
    stmt = (
        select(CV)
        .where(CV.id == test_cv.id)
        .options(joinedload(CV.work_experiences), joinedload(CV.work_experiences))
    )
    result = await db_session.execute(stmt)
    fetched_cv = result.unique().scalar_one()
    assert len(fetched_cv.work_experiences) == 1
    assert fetched_cv.work_experiences[0].job_title == "Фырчатель"

    stmt = (
        select(Company)
        .where(Company.id == test_company.id)
        .options(joinedload(Company.work_experiences), joinedload(Company.work_experiences))
    )
    result = await db_session.execute(stmt)
    fetched_company = result.unique().scalar_one()
    assert len(fetched_company.work_experiences) == 1
