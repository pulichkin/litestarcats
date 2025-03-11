from msgspec import Struct
from uuid import UUID
from typing import Optional


class EducationCreate(Struct):
    cv_id: UUID
    institution_id: UUID
    degree: str
    field_of_study: str
    start_year: int
    end_year: Optional[int] = None
    description: Optional[str] = None


class EducationResponse(Struct):
    id: UUID
    cv_id: UUID
    institution_id: UUID
    degree: str
    field_of_study: str
    start_year: int
    end_year: Optional[int]
    description: Optional[str]
