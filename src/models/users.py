from msgspec import Struct


class UserLogin(Struct, kw_only=True):
    email: str
    password: str


class UserCreate(Struct, kw_only=True):
    first_name: str
    last_name: str
    email: str
    password: str


class UserRead(Struct, kw_only=True):
    id: str
    first_name: str
    last_name: str
    email: str


class UserPatch(Struct, kw_only=True, omit_defaults=True):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
