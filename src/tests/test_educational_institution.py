import pytest
from src.postgres.models.educational_institution import EducationalInstitution


# Тесты для EducationalInstitution
@pytest.mark.asyncio
async def test_create_educational_institution(db_session):
    institution = EducationalInstitution(
        institution_name="New University of LiteStar Cats",
        institution_type="College",
        location="New Cat Town",
    )
    db_session.add(institution)
    await db_session.commit()

    result = await db_session.get(EducationalInstitution, institution.id)
    assert result.institution_name == "New University of LiteStar Cats"
    assert result.institution_type == "College"
