import pytest
from src.postgres.models.cv import CV
from src.postgres.models.user import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload


# Тесты для CV
@pytest.mark.asyncio
async def test_create_cv(db_session, test_user):
    cv = CV(user_id=test_user.id)
    db_session.add(cv)
    await db_session.commit()
    await db_session.refresh(cv)

    result = await db_session.get(CV, cv.id)
    assert result.user_id == test_user.id


@pytest.mark.asyncio
async def test_cv_relationship(db_session, test_user, test_cv):
    stmt = (
        select(User)
        .where(User.id == test_user.id)
        .options(joinedload(User.cvs), joinedload(User.cvs))
    )
    result = await db_session.execute(stmt)
    fetched_user = result.unique().scalar_one()
    assert len(fetched_user.cvs) == 1
    assert fetched_user.cvs[0].id == test_cv.id
