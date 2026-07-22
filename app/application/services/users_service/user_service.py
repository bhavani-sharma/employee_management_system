from application.models.users import UserRequest
from infrastructure.repositories.user_repositories import User_repository
from application.services.users_service.sign_in import SignInService
from application.services.users_service.sign_up import SignUpService
from infrastructure.repositories.employee_repositories import Employee_repository
class UserServices:
    def __init__(self, db):
        self.db = db
        self.repo = User_repository(db)
        self.singin = SignInService(self.repo)
        self.signup = SignUpService(self.repo)
        self.emp_repo = Employee_repository(self.db)

    def user_signup(self, payload: UserRequest):
        return self.signup.execute(payload, self.emp_repo)

    def user_signin(self, username: str, password: str):
        return self.singin.execute(username, password)
    