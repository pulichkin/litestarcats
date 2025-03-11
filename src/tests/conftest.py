import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.postgres.models.cv import CV
from src.postgres.models.user import User
from src.postgres.models.role import Role
from src.postgres.models.company import Company
from src.postgres.models.educational_institution import EducationalInstitution
from litestar.plugins.sqlalchemy import base
from sqlalchemy.orm import sessionmaker


# Настройка тестовой БД
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/ltcats_test_db"


# Фикстура для движка базы данных
@pytest_asyncio.fixture
async def db_engine():
    # Создает движок с подключением к тестовой базе данных
    engine = create_async_engine(
        TEST_DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        echo=True,
    )  # Параметр echo=True включает вывод SQL-запросов в консоль для отладки.
    async with engine.begin() as conn:
        await conn.run_sync(
            base.UUIDBase.metadata.create_all
        )  # Создает все таблицы в базе данных с помощью Base.metadata.create_all.
    yield engine  # Выдает движок для использования в тестах.
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: base.UUIDAuditBase.metadata.drop_all(sync_conn, checkfirst=True))  # После завершения тестов удаляет все таблицы (Base.metadata.drop_all)
    await engine.dispose()  # и освобождает ресурсы движка (engine.dispose()).

@pytest_asyncio.fixture
async def async_session_maker(db_engine):
    return sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

# Фикстура для сессии базы данных
@pytest_asyncio.fixture
async def db_session(async_session_maker) -> AsyncSession:
    AsyncSessionLocal = async_session_maker
    async with AsyncSessionLocal() as session:  # Создает новую сессию базы данных.
        yield session  # Выдает сессию для использования в тестах.
        await session.rollback()


# Фикстуры для создания базовых объектов
@pytest_asyncio.fixture
async def test_user(db_session):
    user = User(first_name="Мурзик", last_name="Котов", email="murzik@example.com")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_role(db_session):
    role = Role(role_name="Соискатель")
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    return role


@pytest_asyncio.fixture
async def test_cv(db_session, test_user):
    cv = CV(user_id=test_user.id)
    db_session.add(cv)
    await db_session.commit()
    return cv


@pytest_asyncio.fixture
async def test_company(db_session):
    company = Company(company_name="Test Cats Corp", industry="IT")
    db_session.add(company)
    await db_session.commit()
    await db_session.refresh(company)
    return company


@pytest_asyncio.fixture
async def test_institution(db_session):
    institution = EducationalInstitution(
        institution_name="Test University of Cats",
        institution_type="Университет",
        location="Test Cats Town",
    )
    db_session.add(institution)
    await db_session.commit()
    await db_session.refresh(institution)
    return institution
