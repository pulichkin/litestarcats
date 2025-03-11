import pytest
from src.postgres.models.user import User
from src.postgres.models.role import Role
from src.postgres.models.user_role import UserRole
from sqlalchemy import select
from sqlalchemy.orm import joinedload


# Тесты для Role
@pytest.mark.asyncio
async def test_create_role(db_session):
    role = Role(role_name="Соискатель")
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    result = await db_session.get(Role, role.id)
    assert result.role_name == "Соискатель"


# Тесты для UserRole
@pytest.mark.asyncio
async def test_create_user_role(db_session, test_user, test_role):
    user_role = UserRole(user_id=test_user.id, role_id=test_role.id)
    db_session.add(user_role)
    await db_session.commit()
    await db_session.refresh(user_role)
    result = await db_session.execute(
        select(UserRole).where(
            UserRole.user_id == test_user.id, UserRole.role_id == test_role.id
        )
    )
    fetched_role = result.scalar()
    assert fetched_role.user_id == test_user.id
    assert fetched_role.role_id == test_role.id


@pytest.mark.asyncio
async def test_user_role_relationship(db_session, test_user, test_role):
    user_role = UserRole(user_id=test_user.id, role_id=test_role.id)
    db_session.add(user_role)
    await db_session.commit()
    await db_session.refresh(user_role)
    await db_session.refresh(test_user)
    # Используем joinedload для предварительной загрузки user и role
    stmt = (
        select(User)
        .where(User.id == test_user.id)
        .options(joinedload(User.user_roles), joinedload(User.user_roles))
    )
    result = await db_session.execute(stmt)
    fetched_user = result.unique().scalar_one()
    assert len(fetched_user.user_roles) == 1
    assert fetched_user.user_roles[0].role.role_name == test_role.role_name
