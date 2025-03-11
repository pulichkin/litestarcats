from msgspec import Struct
from datetime import datetime
from uuid import UUID
from typing import Optional


class WorkExperienceCreate(Struct):
    cv_id: UUID
    company_id: UUID
    job_title: str
    employment_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None


class WorkExperienceResponse(Struct):
    id: UUID
    cv_id: UUID
    company_id: UUID
    job_title: str
    employment_type: str
    start_date: datetime
    end_date: Optional[datetime]
    description: Optional[str]
    created_at: str
    updated_at: str
