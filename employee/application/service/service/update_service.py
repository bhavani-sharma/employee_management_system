from abc import ABC, abstractmethod

from employee.application.model.update_model import EmployeeUpdate
from employee.infrastructure.entity.entity import Employee
from user.application.model.model import CurrentUser


class UpdateService(ABC):
    @abstractmethod
    def update(
        self, employee_id: int, payload: EmployeeUpdate, current_user: CurrentUser
    ) -> Employee: ...
