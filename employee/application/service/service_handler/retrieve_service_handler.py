import logging

from injector import Inject
from sqlalchemy.exc import SQLAlchemyError

from common.exception.exception import EmployeeNotFoundError
from employee.application.model.list_model import EmployeeList, EmployeeSummary
from employee.application.service.service.retrieve_service import (
    RetrieveService,
)
from employee.infrastructure.entity.entity import Employee
from employee.infrastructure.repository.repository import EmployeeRepository
from user.application.model.model import CurrentUser

logger = logging.getLogger("app")


class RetrieveServiceHandler(RetrieveService):
    def __init__(self, repository: Inject[EmployeeRepository]):
        self.repository = repository

    def retrieve(self, employee_id: str, current_user: CurrentUser) -> Employee:
        try:
            employee = self.repository.get_by_id(employee_id)
        except SQLAlchemyError:
            logger.exception("database error while fetching employee")
            raise
        if not employee:
            logger.warning("Employee not found", extra={"employee_id": employee_id})
            raise EmployeeNotFoundError(f"Employee {employee_id} not found")
        logger.info(
            "searched_employee",
            extra={"employee_id": employee_id, "searched_by": current_user.email},
        )
        return employee

    def list(
        self,
        query: EmployeeList,
        current_user: CurrentUser,
    ) -> tuple[list[EmployeeSummary], int]:
        logger.info("retrieved_employees", extra={"reqested_by": current_user.email})
        try:
            return self.repository.list(
                query=query,
            )
        except SQLAlchemyError:
            logger.exception("database error while loading employees")
            raise
