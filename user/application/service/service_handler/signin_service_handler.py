import logging

from injector import Inject

from common.auth.password_hasher import PasswordHasher
from common.auth.service import AuthService
from common.exception.exception import InvalidCredentialsError
from user.application.model.model import UserLogin
from user.application.model.token import Token
from user.application.service.service.signin_service import SignInService
from user.infrastructure.repository.repository import UserRepository

logger = logging.getLogger("app")


class SignInServiceHandler(SignInService):
    def __init__(
        self, repository: Inject[UserRepository], auth_service: Inject[AuthService]
    ):
        self.repository = repository
        self.auth_service = auth_service

    def singin(self, payload: UserLogin):

        user = self.repository.get_by_email(payload.email)
        if not user or not PasswordHasher.verify_password(
            payload.password, user.password_hashed
        ):
            raise InvalidCredentialsError("Incorrect username or password")
        access_token = self.auth_service.create_access_token(data={"sub": user.email})
        logger.info("user signed in", extra={"user": user.email})
        return Token(access_token=access_token)
