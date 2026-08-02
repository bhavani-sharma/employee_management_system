from dataclasses import dataclass


@dataclass(frozen=True)
class AuthConfiguration:
    secret_key: str
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 30
