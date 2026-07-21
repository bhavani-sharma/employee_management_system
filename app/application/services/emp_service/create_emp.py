from app.application.models.employees import EmployeeCreate
import app.infrastructure.schemas.employee_schema as schemas
from app.infrastructure.repositories.employee_repositories import Employee_repository
from app.common.exceptions.exceptions import EmployeeAlreadyExistsError

accepted_roles = ["Admin", "HR", "Manager"]

class CreateEmployeeService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository

    def execute(self, payload: schemas.EmployeeCreate) -> EmployeeCreate:
        if payload.role in accepted_roles:
            payload.is_eligible = True
        if self.repository.get_by_email(payload.email) is not None:
            raise EmployeeAlreadyExistsError("An employee with this email already exists")
        return self.repository.create(payload) 