import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.users import UserCreate
from src.postgres.models.user import User
from msgspec import structs


# Маркируем тест как асинхронный
@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    # Создаем данные для нового пользователя (котика)
    user_data = UserCreate(
        first_name="Васька",  # Имя котика
        last_name="Мурзиков",  # Фамилия котика
        email="vasyamurzikov@whiskers.com",  # Email котика
        password="12345",  # Email котика
    )
    # Создаем объект пользователя из данных
    user = User(**structs.asdict(user_data))
    # Добавляем пользователя в сессию базы данных
    db_session.add(user)
    # Сохраняем изменения в базе данных
    await db_session.commit()
    # Выполняем запрос для получения пользователя по email
    result = await db_session.execute(
        select(User).where(User.email == "vasyamurzikov@whiskers.com")
    )
    # Получаем пользователя из результата запроса
    fetched_user = result.scalar_one()
    # Проверяем, что имя и email пользователя соответствуют ожидаемым значениям
    assert fetched_user.first_name == "Васька"
    assert fetched_user.email == "vasyamurzikov@whiskers.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(db_session: AsyncSession):
    user_data = UserCreate(first_name="Васька", last_name="Мурзиков", email="vasya@whiskers.com")
    user = User(**structs.asdict(user_data), hashed_password=pwd_context.hash("wrong-pass"))
    db_session.add(user)
    await db_session.commit()

    with pytest.raises(HTTPException) as exc:
        await UserController().login(user_data, UsersRepository(session=db_session))
    assert exc.value.status_code == 401
