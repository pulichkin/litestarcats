from msgspec import Struct
from uuid import UUID


class UserRoleCreate(Struct):
    user_id: UUID
    role_id: UUID


class UserRoleResponse(Struct):
    user_id: UUID
    role_id: UUID
