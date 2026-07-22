from application.models.users import UserRequest
from common.exceptions.exceptions import (
    EmployeeNotFoundError,
    EmployeeAlreadyHasUserError,
    EmployeeNotEligibleError,
)
from infrastructure.repositories.user_repositories import User_repository
class SignUpService:
    def __init__(self, repository: User_repository):
        self.repository = repository
    def execute(self, payload: UserRequest, emp_repo):
        employee = emp_repo.get_by_email(payload.email)
        if not employee:
            raise EmployeeNotFoundError(f"Employee {payload.emp_id} not found")
        if not employee.is_eligible:
            raise EmployeeNotEligibleError("This employee is not authorized to become a User")

        user_by_email = self.repository.get_by_email(payload.email)
        if user_by_email:
            raise EmployeeAlreadyHasUserError("This employee already has a user account")

        user_by_emp_id = self.repository.get_by_id(payload.emp_id)
        if user_by_emp_id:
            raise EmployeeAlreadyHasUserError("This employee already has a user account")

        return self.repository.create(payload.email, payload.password, payload.emp_id)
    