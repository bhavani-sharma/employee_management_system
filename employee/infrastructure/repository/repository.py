from abc import ABC, abstractmethod

from employee.application.model.list_model import EmployeeList
from employee.infrastructure.entity.entity import Employee


class EmployeeRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Employee | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Employee | None: ...

    @abstractmethod
    def create(self, data) -> Employee: ...

    @abstractmethod
    def update(self, employee: Employee, data) -> Employee: ...

    @abstractmethod
    def delete(self, employee: Employee) -> None: ...

    @abstractmethod
    def list(self, query: EmployeeList): ...
