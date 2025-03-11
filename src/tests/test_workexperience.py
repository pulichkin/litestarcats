import pytest
from datetime import datetime
from src.postgres.models.company import Company
from src.postgres.models.cv import CV
from src.postgres.models.work_experience import WorkExperience


# Тесты для WorkExperience
@pytest.mark.asyncio
async def test_create_work_experience(db_session, test_cv, test_company):
    work_exp = WorkExperience(
        cv_id=test_cv.id,
        company_id=test_company.id,
        job_title="Developer",
        employment_type="Полная занятость",
        start_date=datetime(2020, 1, 1),
    )
    db_session.add(work_exp)
    await db_session.commit()

    result = await db_session.get(WorkExperience, work_exp.id)
    assert result.job_title == "Developer"
    assert result.cv_id == test_cv.id
    assert result.company_id == test_company.id


@pytest.mark.asyncio
async def test_work_experience_relationship(db_session, test_cv, test_company):
    work_exp = WorkExperience(
        cv_id=test_cv.id,
        company_id=test_company.id,
        job_title="Developer",
        employment_type="Полная занятость",
        start_date=datetime(2021, 1, 1),
    )
    db_session.add(work_exp)
    await db_session.commit()

    cv = await db_session.get(CV, test_cv.id)
    assert len(cv.work_experiences) == 1
    assert cv.work_experiences[0].job_title == "Developer"

    company = await db_session.get(Company, test_company.id)
    assert len(company.work_experiences) == 1
