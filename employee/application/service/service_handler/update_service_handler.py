import logging

from injector import Inject
from sqlalchemy.exc import SQLAlchemyError

from common.exception.exception import (
    CannotDeleteOwnProfileError,
    EmployeeNotFoundError,
)
from employee.application.service.service.retrieve_service import (
    RetrieveService,
)
from employee.application.service.service.update_service import (
    EmployeeUpdate,
    UpdateService,
)
from employee.infrastructure.entity.entity import Employee
from employee.infrastructure.repository.repository import EmployeeRepository
from user.application.model.model import CurrentUser
from user.infrastructure.repository.repository import UserRepository

logger = logging.getLogger("app")
accepted_roles = ["HR", "Manager", "Admin"]


class UpdateServiceHandler(UpdateService):
    def __init__(
        self,
        repository: Inject[EmployeeRepository],
        get_employee_service: Inject[RetrieveService],
        user_repository: Inject[UserRepository],
    ):
        self.repository = repository
        self.get_service = get_employee_service
        self.user_repository = user_repository

    def update(
        self, employee_id: int, payload: EmployeeUpdate, current_user: CurrentUser
    ) -> Employee:
        employee = self.get_service.retrieve(employee_id, current_user)

        # check if manager is valid
        if (
            payload.manager_id is not None
            and self.repository.get_by_id(payload.manager_id) is None
        ):
            logger.warning(
                "Manager not found", extra={"manager_id": payload.manager_id}
            )
            raise EmployeeNotFoundError(
                f"Manager with id '{payload.manager_id}' was not found"
            )
        # update employee.is_eligible
        role = payload.role if payload.role is not None else employee.role
        department = (
            payload.department
            if payload.department is not None
            else employee.department
        )
        if role in accepted_roles or department == "HR":
            employee.is_eligible = True
        else:
            employee.is_eligible = False
        # check if you need to remove user.
        if not employee.is_eligible and employee.id == current_user.employee_id:
            raise CannotDeleteOwnProfileError(
                "This will result in you loosing your user account. You cannot revoke you own system access"
            )
        # remove user if not eligible and not current uesr
        elif not employee.is_eligible and self.user_repository.get_by_employee_id(
            employee.id
        ):
            self.user_repository.delete(employee.email)

        employee.last_modified_by_employee_id = current_user.employee_id
        # update
        logger.info(
            "employee detials updated",
            extra={"employee_id": employee_id, "updated_by": current_user.email},
        )
        try:
            return self.repository.update(employee, payload)
        except SQLAlchemyError:
            logger.exception("database error while updating employee")
            raise
