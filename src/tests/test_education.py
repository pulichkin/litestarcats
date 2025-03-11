import pytest
from src.models.education import EducationCreate
from src.postgres.models.cv import CV
from src.postgres.models.education import Education
from src.postgres.models.educational_institution import EducationalInstitution
from msgspec import structs
from sqlalchemy import select
from sqlalchemy.orm import joinedload


# Тесты для Education
@pytest.mark.asyncio
async def test_create_education(db_session, test_cv, test_institution):
    education_data = EducationCreate(
        cv_id=test_cv.id,
        institution_id=test_institution.id,
        degree="Бакалавр",
        field_of_study="Кошачьих наук",
        start_year=2018,
        end_year=2022,
    )
    education = Education(**structs.asdict(education_data))
    db_session.add(education)
    await db_session.commit()
    await db_session.refresh(education)

    result = await db_session.get(Education, education.id)
    assert result.degree == "Бакалавр"
    assert result.cv_id == test_cv.id
    assert result.institution_id == test_institution.id


@pytest.mark.asyncio
async def test_education_relationship(db_session, test_cv, test_institution):
    education_data = EducationCreate(
        cv_id=test_cv.id,
        institution_id=test_institution.id,
        degree="Бакалавр",
        field_of_study="Кошачьих наук",
        start_year=2018,
        end_year=2022,
    )
    education = Education(**structs.asdict(education_data))
    db_session.add(education)
    await db_session.commit()
    await db_session.refresh(education)
    stmt = (
        select(CV)
        .where(CV.id == test_cv.id)
        .options(joinedload(CV.educations), joinedload(CV.educations))
    )
    result = await db_session.execute(stmt)
    fetched_cv = result.unique().scalar_one()
    assert len(fetched_cv.educations) == 1
    assert fetched_cv.educations[0].degree == "Бакалавр"
    stmt = (
        select(EducationalInstitution)
        .where(EducationalInstitution.id == test_institution.id)
        .options(joinedload(EducationalInstitution.educations), joinedload(EducationalInstitution.educations))
    )
    result = await db_session.execute(stmt)
    fetched_insitution = result.unique().scalar_one()
    assert len(fetched_insitution.educations) == 1
