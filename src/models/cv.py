from msgspec import Struct
from uuid import UUID


class CVCreate(Struct):
    user_id: UUID


class CVResponse(Struct):
    id: UUID
    user_id: UUID
    created_at: str
    updated_at: str
