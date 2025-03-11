import pytest
from src.postgres.models.cv import CV
from src.postgres.models.user import User


# Тесты для CV
@pytest.mark.asyncio
async def test_create_cv(db_session, test_user):
    cv = CV(user_id=test_user.id)
    db_session.add(cv)
    await db_session.commit()

    result = await db_session.get(CV, cv.id)
    assert result.user_id == test_user.id


@pytest.mark.asyncio
async def test_cv_relationship(db_session, test_user, test_cv):
    user = await db_session.get(User, test_user.id)
    assert len(user.cvs) == 1
    assert user.cvs[0].id == test_cv.id
