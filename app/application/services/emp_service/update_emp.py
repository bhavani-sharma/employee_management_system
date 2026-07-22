from infrastructure.schemas.employee_schema import Employee
from application.models.employees import EmployeeUpdate
from infrastructure.repositories.employee_repositories import Employee_repository
from application.services.emp_service.retrieve_emp import GetEmployeeService
from application.services.auth import get_current_user
from infrastructure.schemas.user_schema import Users
from fastapi import Depends
import logging

logger = logging.getLogger("app")


current_user: Users = Depends(get_current_user)
class UpdateEmployeesService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository
        self.get_service = GetEmployeeService(repository)
    def execute(self, employee_id: int, payload: EmployeeUpdate, current_user:Users) -> Employee:
        employee = self.get_service.execute(employee_id, current_user)
        logger.info("updated_employee", extra={"employee_id":employee_id, "updated_by":current_user.email})
        return self.repository.update(employee, payload)
