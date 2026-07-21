from app.application.services import auth
from app.common.exceptions.exceptions import InvalidCredentialsError
from app.infrastructure.repositories.user_repositories import User_repository

class SignInService:
    def __init__(self, repository: User_repository):
        self.repository = repository
    def execute(self,username: str, password: str):
        user = self.repository.get_by_email(username)
        if not user or not auth.verify_password(password, user.password_hashed):
            raise InvalidCredentialsError("Incorrect username or password")
        access_token = auth.create_access_token(data={"sub": user.email})
        return access_token