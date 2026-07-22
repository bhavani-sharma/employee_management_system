from infrastructure.schemas.employee_schema import Employee
from application.models.employees import EmployeeUpdate
from infrastructure.repositories.employee_repositories import Employee_repository
from application.services.emp_service.retrieve_emp import GetEmployeeService
from infrastructure.schemas.user_schema import Users
import logging

logger = logging.getLogger("app")


class UpdateEmployeesService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository
        self.get_service = GetEmployeeService(repository)
    def execute(self, employee_id: int, payload: EmployeeUpdate, current_user:Users, user_repo) -> Employee:
        employee = self.get_service.execute(employee_id, current_user)
        logger.info("updated_employee", extra={"employee_id":employee_id, "updated_by":current_user.email})
        return self.repository.update(employee, payload, user_repo)
