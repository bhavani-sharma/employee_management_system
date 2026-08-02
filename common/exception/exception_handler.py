import logging
from typing import ClassVar

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from common.exception.exception import (
    CannotDeleteOwnProfileError,
    DatabaseOperationError,
    DuplicatePanNumberError,
    EmployeeAlreadyExistsError,
    EmployeeAlreadyHasUserError,
    EmployeeNotEligibleError,
    EmployeeNotFoundError,
    InformationValidationError,
    InvalidCredentialsError,
)

logger = logging.getLogger("app.exceptions")


class ExceptionHandlers:
    STATUS_CODES: ClassVar[dict[type[Exception], int]] = {
        EmployeeNotFoundError: status.HTTP_404_NOT_FOUND,
        EmployeeAlreadyExistsError: status.HTTP_409_CONFLICT,
        EmployeeNotEligibleError: status.HTTP_403_FORBIDDEN,
        EmployeeAlreadyHasUserError: status.HTTP_409_CONFLICT,
        CannotDeleteOwnProfileError: status.HTTP_403_FORBIDDEN,
        InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
        InformationValidationError: status.HTTP_400_BAD_REQUEST,
        DuplicatePanNumberError: status.HTTP_409_CONFLICT,
        DatabaseOperationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    def register(self, app: FastAPI) -> None:
        for exception_type in self.STATUS_CODES:
            app.add_exception_handler(exception_type, self.handle_domain_exception)
        # Enum validarion is performed by Pydantic, which raises RequestValidationError.
        # Registering this handler changes FastAPI's default 422 response to 400.
        app.add_exception_handler(
            RequestValidationError, self.validation_exception_handler
        )
        app.add_exception_handler(Exception, self.global_exception_handlers)

    async def handle_domain_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:
        status_code = self.STATUS_CODES[type(exc)]
        headers = (
            {"WWW-Authenticate": "Bearer"}
            if isinstance(exc, InvalidCredentialsError)
            else None
        )
        content = (
            {"detail": "Unable to complete the database operation"}
            if isinstance(exc, DatabaseOperationError)
            else {"detail": str(exc)}
        )
        return JSONResponse(status_code=status_code, content=content, headers=headers)

    async def global_exception_handlers(self, request: Request, exc: Exception):
        logger.exception(
            "Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    @staticmethod
    async def validation_exception_handler(request, exc: RequestValidationError):

        logger.warning(
            "Request validation failed",
            extra={
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors(),
            },
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Validation failed", "errors": exc.errors()},
        )
