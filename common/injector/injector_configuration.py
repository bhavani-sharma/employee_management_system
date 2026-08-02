import os

from dotenv import load_dotenv
from fastapi_injector import request_scope
from injector import CallableProvider, Injector, Module, singleton
from sqlalchemy.orm import Session

from common.auth.configuration import AuthConfiguration
from common.auth.service import AuthService
from common.data.database import SessionLocal
from employee.application.service.service.create_service import (
    CreateService,
)
from employee.application.service.service.delete_service import (
    DeleteService,
)
from employee.application.service.service.retrieve_service import (
    RetrieveService,
)
from employee.application.service.service.update_service import (
    UpdateService,
)
from employee.application.service.service_handler.create_service_handler import (
    CreateServiceHandler,
)
from employee.application.service.service_handler.delete_service_handler import (
    DeleteServiceHandler,
)
from employee.application.service.service_handler.retrieve_service_handler import (
    RetrieveServiceHandler,
)
from employee.application.service.service_handler.update_service_handler import (
    UpdateServiceHandler,
)
from employee.infrastructure.repository.repository import EmployeeRepository
from employee.infrastructure.repository.repository_handler import (
    EmployeeRepositoryHandler,
)
from user.application.service.service.signin_service import SignInService
from user.application.service.service.signup_service import SignUpService
from user.application.service.service_handler.signin_service_handler import (
    SignInServiceHandler,
)
from user.application.service.service_handler.singup_service_handler import (
    SignUpServiceHandler,
)
from user.infrastructure.repository.repository import UserRepository
from user.infrastructure.repository.repository_handler import UserRepositoryHandler


def provide_session() -> Session:
    return SessionLocal()


class AppModule(Module):
    def configure(self, binder):
        load_dotenv()

        settings = AuthConfiguration(
            secret_key=os.environ["SECRET_KEY"],
            access_token_expires_minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]),
        )

        binder.bind(Session, to=CallableProvider(provide_session), scope=request_scope)
        binder.bind(
            EmployeeRepository, to=EmployeeRepositoryHandler, scope=request_scope
        )
        binder.bind(UserRepository, to=UserRepositoryHandler, scope=request_scope)

        # binding services to its concrete classes
        # employee_service
        binder.bind(CreateService, to=CreateServiceHandler, scope=request_scope)
        binder.bind(
            RetrieveService,
            to=RetrieveServiceHandler,
            scope=request_scope,
        )
        binder.bind(UpdateService, to=UpdateServiceHandler, scope=request_scope)
        binder.bind(DeleteService, to=DeleteServiceHandler, scope=request_scope)

        # user_service
        binder.bind(SignInService, to=SignInServiceHandler, scope=request_scope)
        binder.bind(SignUpService, to=SignUpServiceHandler, scope=request_scope)

        binder.bind(AuthConfiguration, to=settings, scope=singleton)
        binder.bind(AuthService, to=AuthService, scope=request_scope)
        return super().configure(binder)


def create_injector() -> Injector:
    return Injector([AppModule()], auto_bind=False)
