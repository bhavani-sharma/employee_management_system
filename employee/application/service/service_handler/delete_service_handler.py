import logging

from injector import Inject
from sqlalchemy.exc import SQLAlchemyError

from common.exception.exception import CannotDeleteOwnProfileError
from employee.application.service.service.delete_service import (
    DeleteService,
)
from employee.application.service.service.retrieve_service import (
    RetrieveService,
)
from employee.infrastructure.repository.repository import EmployeeRepository
from user.application.model.model import CurrentUser

logger = logging.getLogger("app")


class DeleteServiceHandler(DeleteService):
    def __init__(
        self,
        repository: Inject[EmployeeRepository],
        get_service: Inject[RetrieveService],
    ):
        self.repository = repository
        self.get_service = get_service

    def delete(self, id: int, current_user: CurrentUser) -> None:
        employee = self.get_service.retrieve(id, current_user)

        if current_user.employee_id == id:
            logger.warning(
                "User tried deleting own record",
                extra={"employee_id": current_user.employee_id},
            )
            raise CannotDeleteOwnProfileError(
                "You cannot delete the employee record linked to your own account"
            )
        try:
            self.repository.delete(employee)
        except SQLAlchemyError:
            logger.exception("database error while deleting employee")
            raise
        logger.info(
            "employee_deleted",
            extra={"employee_id": id, "deleted_by": current_user.email},
        )
