from abc import ABC, abstractmethod

from user.application.model.model import CurrentUser


class DeleteService(ABC):
    @abstractmethod
    def delete(self, employee_id: str, current_user: CurrentUser) -> None: ...
