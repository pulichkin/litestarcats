import pytest
from src.postgres.models.user import User
from src.postgres.models.role import Role
from src.postgres.models.user_role import UserRole
from sqlalchemy import select


# Тесты для Role
@pytest.mark.asyncio
async def test_create_role(db_session):
    role = Role(role_name="Соискатель")
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    result = await db_session.execute(
        select(Role).where(Role.id == role.id)
    )
    fetched = result.scalar_one()
    assert fetched.role_name == "Соискатель"


# Тесты для UserRole
@pytest.mark.asyncio
async def test_create_user_role(db_session, test_user, test_role):
    user_role = UserRole(user_id=test_user.id, role_id=test_role.id)
    db_session.add(user_role)
    await db_session.commit()

    result = await db_session.execute(
        select(UserRole).where(
            UserRole.user_id == test_user.id, UserRole.role_id == test_role.id
        )
    )
    assert result.scalar_one().user_id == test_user.id
    assert result.scalar_one().role_id == test_role.id


@pytest.mark.asyncio
async def test_user_role_relationship(db_session, test_user, test_role):
    user_role = UserRole(user_id=test_user.id, role_id=test_role.id)
    db_session.add(user_role)
    await db_session.commit()

    user = await db_session.get(User, test_user.id)
    assert len(user.roles) == 1
    assert user.roles[0].role_name == test_role.role_name
