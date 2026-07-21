from app.infrastructure.schemas.user_schema import Users
from app.common.exceptions.exceptions import CannotDeleteOwnProfileError
from app.infrastructure.repositories.employee_repositories import Employee_repository
from app.application.services.emp_service.retrieve_emp import GetEmployeeService


class DeleteEmployeeService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository
        self.get_service = GetEmployeeService(repository)

    def execute(self, employee_id: int, current_user: Users) -> None:
        employee = self.get_service.get_employee(employee_id)
 
        if current_user.emp_id == employee_id:
            raise CannotDeleteOwnProfileError("You cannot delete the employee record linked to your own account")
 
        self.repository.delete(employee)