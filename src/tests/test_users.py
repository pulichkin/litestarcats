import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.users import UserCreate, UserLogin
from src.postgres.models.user import User
from msgspec import structs
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["sha256_crypt"])


# Маркируем тест как асинхронный
@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    # Создаем данные для нового пользователя (котика)
    user_data = UserCreate(
        first_name="Васька",  # Имя котика
        last_name="Мурзиков",  # Фамилия котика
        email="vasyamurzikov@whiskers.com",  # Email котика
        password="12345",  # Пароль котика
    )
    # Создаем объект пользователя из данных
    user_data = structs.asdict(user_data)
    password = user_data.pop("password", None)
    user = User(**user_data, hashed_password=pwd_context.hash(password))
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
async def test_login_invalid_credentials(db_session: AsyncSession, test_client):
    # 1. Создаем пользователя с некорректным паролем
    user_data = UserCreate(
        first_name="Васька",
        last_name="Мурзиков",
        email="vasyamurzikov@whiskers.com",
        password="12345",
    )
    user_dict = structs.asdict(user_data)
    password = user_dict.pop("password")
    user = User(**user_dict, hashed_password=pwd_context.hash("wrong-pass"))
    db_session.add(user)
    await db_session.commit()

    # Данные для логина
    login_data = UserLogin(email=user.email, password=password)

    # Отправка POST-запроса через тестовый клиент
    response = await test_client.post("/users/login", json=structs.asdict(login_data))

    # Проверка результата
    assert response.status_code == 401
    assert response.json().get("detail") == "Неверный email или пароль"
