import logging
from infrastructure.schemas.user_schema import Users
from application.models.employees import EmployeeCreate
import infrastructure.schemas.employee_schema as schemas
from infrastructure.repositories.employee_repositories import Employee_repository
from common.exceptions.exceptions import EmployeeAlreadyExistsError


logger = logging.getLogger("app")
accepted_roles = ["Admin", "HR", "Manager"]

class CreateEmployeeService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository

    def execute(self, payload: schemas.EmployeeCreate, current_user:Users) -> EmployeeCreate:
        if payload.role in accepted_roles:
            payload.is_eligible = True
        if self.repository.get_by_email(payload.email) is not None:
            raise EmployeeAlreadyExistsError("An employee with this email already exists")

        created_employee = self.repository.create(payload)
        logger.info("employee created", extra={"employee_id": payload.emp_id, "email": payload.email, "created_by": current_user.email})
        return created_employee 