from abc import ABC, abstractmethod

from user.application.model.model import UserRequest
from user.infrastructure.entity.entity import User


class SignUpService(ABC):
    @abstractmethod
    def signup(self, payload: UserRequest) -> User: ...
