import app.application.models.employees as Employees
from sqlalchemy.orm import Session
import app.infrastructure.schemas.employee_schema as empschema
from app.infrastructure.schemas.user_schema import Users
from app.infrastructure.repositories.employee_repositories import Employee_repository
from typing import List, Tuple
from datetime import date
from app.application.services.emp_service.create_emp import CreateEmployeeService
from app.application.services.emp_service.retrieve_emp import GetEmployeeService
from app.application.services.emp_service.update_emp import UpdateEmployeesService
from app.application.services.emp_service.delete_emp import DeleteEmployeeService

# repo = Employee_repository()

class CreateEmployee:
    def __init__(self, db:Session):
        repo = Employee_repository(db)
        self.create = CreateEmployeeService(repo)
        self.retrieve = GetEmployeeService(repo)
        self.update = UpdateEmployeesService(repo)
        self.delete = DeleteEmployeeService(repo)

    def create_employee(self, payload: Employees.EmployeeCreate) -> empschema.Employee:
        return self.create.execute(payload)
 
    def get_employee(self, employee_id: str) -> empschema.Employee:
        return self.retrieve.execute(employee_id)
    

    def list_employees(self, page: int, page_size: int) -> Tuple[List[empschema.Employee], int]:
        return self.retrieve.list_employees(page, page_size)
 

    def update_employee(self, employee_id: int, payload: Employees.EmployeeUpdate) -> empschema.Employee:
        return self.update.execute(employee_id, payload)
    

    def delete_employee(self, employee_id: str, current_user: Users) -> None:
        return self.delete.execute(employee_id, current_user)
    
    def format_salary(value:float)->str:
        return f"₹{value:,.2f}"
    
    def format_date(value: date)->str:
        return value.strftime("%d-%m-%Y")
