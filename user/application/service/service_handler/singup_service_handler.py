import logging

from injector import Inject

from common.auth.password_hasher import PasswordHasher
from common.auth.service import AuthService
from common.exception.exception import (
    EmployeeAlreadyHasUserError,
    EmployeeNotEligibleError,
    EmployeeNotFoundError,
    InformationValidationError,
)
from employee.infrastructure.repository.repository import EmployeeRepository
from user.application.model.model import UserRequest
from user.application.service.service.signup_service import SignUpService
from user.infrastructure.repository.repository import UserRepository

logger = logging.getLogger("app")


class SignUpServiceHandler(SignUpService):
    def __init__(
        self,
        repository: Inject[UserRepository],
        employee_repository: Inject[EmployeeRepository],
        auth_service: Inject[AuthService],
    ):
        self.repository = repository
        self.employee_repository = employee_repository
        self.auth_service = auth_service

    def signup(self, payload: UserRequest):
        employee_by_id = self.employee_repository.get_by_id(payload.employee_id)
        if not employee_by_id:
            raise EmployeeNotFoundError(f"Employee {payload.employee_id} not found")
        if employee_by_id.email.casefold() != payload.email.casefold():
            raise InformationValidationError(
                "The email address does not match the employee ID"
            )

        
        employee_by_email = self.employee_repository.get_by_email(payload.email)
        if not employee_by_email:
            raise EmployeeNotFoundError(f"Employee {payload.employee_id} not found")
        if not employee_by_email.is_eligible:
            raise EmployeeNotEligibleError(
                "This employee is not authorized to become a User"
            )

        user_by_email = self.repository.get_by_email(payload.email)
        if user_by_email:
            raise EmployeeAlreadyHasUserError(
                "This employee already has a user account"
            )
        logger.info("user signed up", extra={"user": payload.email})
        return self.repository.create(
            payload.email,
            PasswordHasher.hash_password(payload.password),
            payload.employee_id,
        )
