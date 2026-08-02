import logging

from injector import Inject
from sqlalchemy.exc import SQLAlchemyError

from common.exception.exception import EmployeeNotFoundError
from employee.application.model.create_model import EmployeeCreate
from employee.application.service.service.create_service import CreateService
from employee.infrastructure.entity.entity import Employee
from employee.infrastructure.repository.repository import EmployeeRepository
from user.application.model.model import CurrentUser

logger = logging.getLogger("app")
accepted_roles = ["Admin", "Manager"]


class CreateServiceHandler(CreateService):
    def __init__(self, repository: Inject[EmployeeRepository]):
        self.repository = repository

    def create(self, payload: EmployeeCreate, current_user: CurrentUser) -> Employee:
        new_employee = Employee(**payload.model_dump())
        # adding created by and last modified by
        new_employee.created_by_employee_id = current_user.employee_id
        new_employee.last_modified_by_employee_id = current_user.employee_id
        # checking if employee is eligible
        if new_employee.role in accepted_roles:
            new_employee.is_eligible = True
        else:
            new_employee.is_eligible = False
        if self.repository.get_by_email(payload.email) is not None:
            logger.warning("Email id already in use", extra={"email id": payload.email})

        if (
            self.repository.get_by_id(payload.manager_id) is None
            and payload.manager_id is not None
        ):
            logger.warning(
                "Manager not found", extra={"manager_id": payload.manager_id}
            )
            raise EmployeeNotFoundError(
                f"Manager with id '{payload.manager_id}' was not found"
            )
        try:
            created_employee = self.repository.create(new_employee)
        except SQLAlchemyError:
            logger.exception("database error while creating employee")
            raise
        logger.info(
            "employee created",
            extra={
                "employee_id": created_employee.id,
                "email": created_employee.email,
                "created_by": current_user.email,
            },
            exc_info=True,  # noqa: LOG014
        )
        return created_employee
