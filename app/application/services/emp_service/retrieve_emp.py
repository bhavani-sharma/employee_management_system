
from infrastructure.repositories.employee_repositories import Employee_repository
from typing import List, Tuple
import infrastructure.schemas.employee_schema as empschema
from common.exceptions.exceptions import EmployeeNotFoundError
from infrastructure.schemas.user_schema import Users
import logging


logger = logging.getLogger("app")
class GetEmployeeService:
    def __init__(self, repository:Employee_repository ):
        self.repository = repository
    def execute(self, employee_id: str, current_user:Users) -> empschema.Employee:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Employee {employee_id} not found")
        logger.info("searched_employee", extra={"employee_id": employee_id, "searched_by":current_user.email} )
        return employee
    

    def list_employees(self, page: int, page_size: int, current_user:Users) -> Tuple[List[empschema.Employee], int]:
        logger.info("retrieved_all_employees", extra={"reqested_by":current_user.email})
        return self.repository.get_page(page, page_size)