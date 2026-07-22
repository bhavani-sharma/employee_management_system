from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Type
import logging
from common.exceptions.exceptions import (CannotDeleteOwnProfileError, 
                               EmployeeAlreadyExistsError,
                               EmployeeAlreadyHasUserError,
                               EmployeeNotEligibleError,
                               EmployeeNotFoundError,
                               InvalidCredentialsError
)

logger = logging.getLogger("app.exceptions")

# def register_exception_handlers(app:FastAPI)->None:
#     @app.exception_handler(EmployeeNotFoundError)
#     async def handle_not_found(request: Request, exc: EmployeeNotFoundError)->JSONResponse:
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail":str(exc)})
    
#     @app.exception_handler(EmployeeAlreadyExistsError)
#     async def bad_request(request: Request, exc: EmployeeAlreadyExistsError)->JSONResponse:
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":str(exc)})
    
#     @app.exception_handler(EmployeeNotEligibleError)
#     async def forbidden(request: Request, exc: EmployeeNotEligibleError)->JSONResponse:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail":str(exc)})
    
#     @app.exception_handler(EmployeeAlreadyHasUserError)
#     async def already_has_user(request: Request, exc: EmployeeAlreadyHasUserError)->JSONResponse:
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":str(exc)})
    
#     @app.exception_handler(CannotDeleteOwnProfileError)
#     async def cannot_delete(request: Request, exc: CannotDeleteOwnProfileError)->JSONResponse:
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail":str(exc)})
    
#     @app.exception_handler(InvalidCredentialsError)
#     async def unauthorized(request: Request, exc: InvalidCredentialsError)->JSONResponse:
#         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail":str(exc)},
#                                                                                headers={"WWW-Authenticate":"Bearer"})

class ExceptionHandlers:
    STATUS_CODES: Dict[Type[Exception], int]={
    EmployeeNotFoundError: status.HTTP_404_NOT_FOUND,
    EmployeeAlreadyExistsError: status.HTTP_400_BAD_REQUEST,
    EmployeeNotEligibleError: status.HTTP_403_FORBIDDEN,
    EmployeeAlreadyHasUserError: status.HTTP_400_BAD_REQUEST,
    CannotDeleteOwnProfileError: status.HTTP_403_FORBIDDEN,
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,

}
    def register(self, app: FastAPI)->None:
        for exception_type in self.STATUS_CODES:
            app.add_exception_handler(exception_type, self.handle_domain_exception)

    async def handle_domain_exception(self, request:Request, exc: Exception)->JSONResponse:
        status_code = self.STATUS_CODES[type(exc)]
        headers = {"WWW-Authenticate": "Bearer"} if isinstance(exc, InvalidCredentialsError) else None
        return JSONResponse(status_code=status_code, content={"detail": str(exc)}, headers=headers)