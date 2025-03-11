import pytest
from src.postgres.models.cv import CV
from src.postgres.models.education import Education
from src.postgres.models.educational_institution import EducationalInstitution


# Тесты для Education
@pytest.mark.asyncio
async def test_create_education(db_session, test_cv, test_institution):
    education = Education(
        cv_id=test_cv.id,
        institution_id=test_institution.id,
        degree="Bachelor",
        field_of_study="Computer Science",
        start_year=2018,
        end_year=2022,
    )
    db_session.add(education)
    await db_session.commit()

    result = await db_session.get(Education, education.id)
    assert result.degree == "Bachelor"
    assert result.cv_id == test_cv.id
    assert result.institution_id == test_institution.id


@pytest.mark.asyncio
async def test_education_relationship(db_session, test_cv, test_institution):
    education = Education(
        cv_id=test_cv.id,
        institution_id=test_institution.id,
        degree="Bachelor",
        field_of_study="Computer Science",
        start_year=2018,
        end_year=2022,
    )
    db_session.add(education)
    await db_session.commit()

    cv = await db_session.get(CV, test_cv.id)
    assert len(cv.educations) == 1
    assert cv.educations[0].degree == "Bachelor"

    institution = await db_session.get(EducationalInstitution, test_institution.id)
    assert len(institution.educations) == 1
