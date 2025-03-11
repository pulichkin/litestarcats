from msgspec import Struct
from uuid import UUID
from typing import Optional


class CompanyCreate(Struct):
    company_name: str
    industry: str
    logo_url: Optional[str] = None
    address: Optional[str] = None


class CompanyResponse(Struct):
    id: UUID
    company_name: str
    industry: str
    logo_url: Optional[str]
    address: Optional[str]
    created_at: str
    updated_at: str
