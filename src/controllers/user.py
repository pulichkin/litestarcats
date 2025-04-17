import logging
from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import HTTPException
from src.models.users import UserCreate, UserLogin, UserPatch, UserRead
from src.postgres.models.user import User
from src import app
from msgspec import json, structs, to_builtins
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import (
    filters,
    repository,
)
from passlib.context import CryptContext
from uuid import UUID
from litestar.dto import MsgspecDTO
from src.clients.cache import keydb
from litestar.response import Template


logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["sha256_crypt"])


class UsersRepository(repository.SQLAlchemyAsyncRepository[User]):
    """Author repository."""

    model_type = User


async def provide_users_repo(db_session: AsyncSession) -> UsersRepository:
    """This provides the default Authors repository."""
    return UsersRepository(session=db_session)


class UserController(Controller):
    path = "/users"
    dependencies = {
            "users_repo": Provide(provide_users_repo),
            }

    @get(path="/", return_dto=MsgspecDTO[UserRead])
    async def list_users(
        self,
        users_repo: UsersRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[UserRead]:
        """List authors."""
        results, total = await users_repo.list_and_count(limit_offset)
        return OffsetPagination[UserRead](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post("/login", signature_types=[User])  # Отключаем защиту для логина
    async def login(
            self,
            data: UserLogin,
            users_repo: UsersRepository,
            ) -> dict:
        user = await users_repo.get_one_or_none(email=data.email)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный email или пароль")
        token = app.jwt_auth.create_token(identifier=str(user.id))
        return {"access_token": token, "token_type": "bearer"}

    @post("/", return_dto=MsgspecDTO[UserRead])
    async def create_user(self, data: UserCreate, users_repo: UsersRepository) -> UserRead:
        user_data = structs.asdict(data)
        password = user_data.pop("password", None)
        user = await users_repo.add(
            User(**user_data, hashed_password=pwd_context.hash(password)),
        )
        await users_repo.session.commit()
        return user

    @get("/{user_id:uuid}", return_dto=MsgspecDTO[UserRead])
    async def get_user(
        self,
        user_id: UUID,
        users_repo: UsersRepository,
    ) -> UserRead:
        """Get an existing author."""
        cache_key = f"user:{user_id}"
        cached = await keydb.get(cache_key)
        if cached:
            return json.decode(cached, type=UserRead)
        user = await users_repo.get(user_id)
        await keydb.set(cache_key, json.encode(user.to_dict()), ex=3600)  # Кэш на час
        return user

    @patch("/{user_id:uuid}", return_dto=MsgspecDTO[UserRead])
    async def update_user(
        self, user_id: UUID, data: UserPatch, users_repo: UsersRepository
    ) -> UserRead:
        try:
            raw_obj = to_builtins(data)
            raw_obj["id"] = user_id
            user = User(**raw_obj)
            updated_user = await users_repo.update(user)
            await users_repo.session.commit()
            return updated_user
        except IntegrityError as e:
            # Если нарушен уникальный индекс (например, email уже существует)
            raise HTTPException(status_code=400, detail="Email already exists")
        except Exception as e:
            # Другие ошибки
            raise HTTPException(status_code=500, detail="Internal server error")

    @delete("/{user_id:uuid}")
    async def delete_user(self, user_id: UUID, users_repo: UsersRepository) -> None:
        await users_repo.delete(user_id)
        await users_repo.session.commit()

    @get("/{user_id:uuid}/cv", media_type="text/html")
    async def get_user_resume(self, user_id: UUID, users_repo: UsersRepository) -> Template:
        user = await users_repo.get(user_id)
        template = app.env.get_template("cv.html")
        return Template(template=template, context={"user": user})
