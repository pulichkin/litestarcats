from .role import Role  # Сначала импортируем Role, если он есть
from .user_role import UserRole  # Затем UserRole, так как он зависит от User и Role
from .company import Company
from .work_experience import WorkExperience
from .educational_institution import EducationalInstitution
from .education import Education
from .cv import CV
from .user import User  # Наконец User, так как он зависит от UserRole

from sqlalchemy.orm import configure_mappers

# Явно вызываем configure_mappers после импорта всех моделей
configure_mappers()
