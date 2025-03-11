from msgspec import Struct
from uuid import UUID


class RoleCreate(Struct):
    role_name: str


class RoleResponse(Struct):
    id: UUID
    role_name: str
