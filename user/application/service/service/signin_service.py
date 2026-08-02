from abc import ABC, abstractmethod
from contextvars import Token

from user.application.model.model import UserLogin


class SignInService(ABC):
    @abstractmethod
    def singin(self, payload: UserLogin) -> Token: ...
