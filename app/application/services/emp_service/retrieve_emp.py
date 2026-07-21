
from app.infrastructure.repositories.employee_repositories import Employee_repository
from typing import List, Tuple
import app.infrastructure.schemas.employee_schema as empschema
from app.common.exceptions.exceptions import EmployeeNotFoundError
# def get_all(skip:int = 0, limit:int = 100, db:Session = Depends(get_db), current_user:Users = Depends(get_current_user)):
#     return db.query(Employee).offset(skip).limit(limit).all()

class GetEmployeeService:
    def __init__(self, repository:Employee_repository ):
        self.repository = repository
    def execute(self, employee_id: str) -> empschema.Employee:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee {employee_id} not found")
        return employee
    

    def list_employees(self, page: int, page_size: int) -> Tuple[List[empschema.Employee], int]:
        return self.repository.get_page(page, page_size)