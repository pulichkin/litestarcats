from litestar import Controller, get, post, patch, delete
from litestar.di import Provide
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import HTTPException
from src.models.users import UserCreate, UserPatch
from src.postgres.models.user import User
from msgspec import structs, to_builtins
from litestar.pagination import OffsetPagination
from litestar.plugins.sqlalchemy import (
    filters,
    repository,
)
from uuid import UUID


class UsersRepository(repository.SQLAlchemyAsyncRepository[User]):
    """Author repository."""

    model_type = User


async def provide_users_repo(db_session: AsyncSession) -> UsersRepository:
    """This provides the default Authors repository."""
    return UsersRepository(session=db_session)


class UserController(Controller):
    path = "/users"
    dependencies = {"users_repo": Provide(provide_users_repo)}

    @get(path="/")
    async def list_users(
        self,
        users_repo: UsersRepository,
        limit_offset: filters.LimitOffset,
    ) -> OffsetPagination[User]:
        """List authors."""
        results, total = await users_repo.list_and_count(limit_offset)
        return OffsetPagination[User](
            items=results,
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )

    @post("/")
    async def create_user(self, data: UserCreate, users_repo: UsersRepository) -> User:
        user = await users_repo.add(
            User(**structs.asdict(data)),
        )
        await users_repo.session.commit()
        return user

    @get("/{user_id:uuid}")
    async def get_user(
        self,
        user_id: UUID,
        users_repo: UsersRepository,
    ) -> User:
        """Get an existing author."""
        user = await users_repo.get(user_id)
        return user

    @patch("/{user_id:uuid}")
    async def update_user(
        self, user_id: UUID, data: UserPatch, users_repo: UsersRepository
    ) -> User:
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
