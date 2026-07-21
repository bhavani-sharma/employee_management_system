from app.infrastructure.schemas.employee_schema import Employee
from app.application.models.employees import EmployeeUpdate
from app.infrastructure.repositories.employee_repositories import Employee_repository
from app.application.services.emp_service.retrieve_emp import GetEmployeeService

class UpdateEmployeesService:
    def __init__(self, repository: Employee_repository):
        self.repository = repository
        self.get_service = GetEmployeeService(repository)
    def execute(self, employee_id: int, payload: EmployeeUpdate) -> Employee:
        employee = self.get_service.execute(employee_id)
        return self.repository.update(employee, payload)
