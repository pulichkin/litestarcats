from msgspec import Struct


class UserCreate(Struct, kw_only=True):
    first_name: str
    last_name: str
    email: str


class UserPatch(Struct, kw_only=True, omit_defaults=True):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
