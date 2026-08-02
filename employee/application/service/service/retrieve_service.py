from abc import ABC, abstractmethod

from employee.application.model.list_model import EmployeeList, EmployeeSummary
from employee.infrastructure.entity.entity import Employee
from user.application.model.model import CurrentUser


class RetrieveService(ABC):
    @abstractmethod
    def retrieve(self, employee_id: str, current_user: CurrentUser) -> Employee: ...

    @abstractmethod
    def list(
        self,
        query: EmployeeList,
        current_user: CurrentUser,
    ) -> tuple[list[EmployeeSummary], int]: ...
