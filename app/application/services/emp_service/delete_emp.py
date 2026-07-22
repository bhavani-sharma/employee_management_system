from infrastructure.schemas.user_schema import Users
from common.exceptions.exceptions import CannotDeleteOwnProfileError
from infrastructure.repositories.employee_repositories import Employee_repository
from application.services.emp_service.retrieve_emp import GetEmployeeService
import logging


logger = logging.getLogger("app")

class DeleteEmployeeService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository
        self.get_service = GetEmployeeService(repository)

    def execute(self, employee_id: str, current_user: Users) -> None:
        employee = self.get_service.execute(employee_id, current_user)
 
        if current_user.emp_id == employee_id:
            raise CannotDeleteOwnProfileError("You cannot delete the employee record linked to your own account")
 
        self.repository.delete(employee)
        logger.info("employee_deleted", extra={"employee_id":employee_id, "deleted_by": current_user.email})