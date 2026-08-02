from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_injector import Injected

from common.auth.service import AuthService
from common.context.request_context import RequestContext
from common.exception.exception import InvalidCredentialsError
from user.application.model.model import CurrentUser
from user.infrastructure.repository.repository import UserRepository

security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_service: AuthService = Injected(AuthService),  # noqa: B008
    user_repository: UserRepository = Injected(UserRepository),  # noqa: B008
) -> CurrentUser:
    payload = auth_service.decode_access_token(credentials.credentials)
    user = user_repository.get_by_email(payload["sub"])

    if user is None:
        # A token for a deleted account is an authentication failure, not a
        # disclosure that an employee record no longer exists.
        raise InvalidCredentialsError("Current user account no longer exists")

    RequestContext.set_current_user(user)
    return user
