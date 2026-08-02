from abc import ABC, abstractmethod

from employee.application.model.create_model import EmployeeCreate
from employee.infrastructure.entity.entity import Employee
from user.application.model.model import CurrentUser


class CreateService(ABC):
    @abstractmethod
    def create(
        self, payload: EmployeeCreate, current_user: CurrentUser
    ) -> Employee: ...
