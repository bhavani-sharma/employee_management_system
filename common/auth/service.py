import logging
from datetime import datetime, timedelta, timezone

from injector import Inject
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from common.auth.configuration import AuthConfiguration
from common.exception.exception import InvalidCredentialsError

logger = logging.getLogger("app.auth")


class AuthService:
    def __init__(
        self,
        settings: Inject[AuthConfiguration],
    ):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expires_minutes = settings.access_token_expires_minutes

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        payload = data.copy()
        payload["exp"] = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=self.access_token_expires_minutes)
        )
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict:

        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            if payload.get("sub") is None:
                raise InvalidCredentialsError("Invalid Access Token")

            return payload

        except ExpiredSignatureError:
            raise InvalidCredentialsError("Access token has Expired")

        except JWTError:
            raise InvalidCredentialsError("Invalid access token")
