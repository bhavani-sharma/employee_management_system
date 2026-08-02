from abc import ABC, abstractmethod

from user.infrastructure.entity.entity import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def create(self, email: str, password_hash: str, employee_id: int) -> User: ...

    @abstractmethod
    def delete(self, email: str) -> None: ...

    @abstractmethod
    def get_by_employee_id(self, employee_id: int) -> User | None: ...
