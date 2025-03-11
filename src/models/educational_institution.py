from msgspec import Struct
from uuid import UUID
from typing import Optional


class EducationalInstitutionCreate(Struct):
    institution_name: str
    institution_type: str
    location: str
    website: Optional[str] = None
    accreditation: Optional[str] = None


class EducationalInstitutionResponse(Struct):
    id: UUID
    institution_name: str
    institution_type: str
    location: str
    website: Optional[str]
    accreditation: Optional[str]
    created_at: str
    updated_at: str
