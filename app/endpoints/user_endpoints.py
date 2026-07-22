from fastapi import APIRouter, Depends, status      
import application.models.users as models
import application.models.tokens as tokens
from common.exceptions.exceptions import (
    EmployeeAlreadyHasUserError,
    EmployeeNotEligibleError,
    EmployeeNotFoundError,
    InvalidCredentialsError,
)
from application.services.users_service.user_service import UserServices
from infrastructure.dependencies import get_user_service


router = APIRouter(prefix="/auth", tags=["auth"])

#signup
@router.post("/signup", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload:models.UserRequest,service: UserServices = Depends(get_user_service)):
    try:
        return service.user_signup(payload)
    except EmployeeNotFoundError :
        raise EmployeeNotFoundError("Employee Not Found")
    except EmployeeNotEligibleError:
        raise EmployeeNotEligibleError("Employee Not Eligible")
    except EmployeeAlreadyHasUserError:
        raise EmployeeAlreadyHasUserError("Employee Already Has User")
    

@router.post("/signin", response_model=tokens.Token)
def signin(form_data: models.UserLogin= Depends(),service: UserServices = Depends(get_user_service)):
    try:
        access_token = service.user_signin(form_data.email, form_data.password)
    except InvalidCredentialsError:
        raise InvalidCredentialsError("Incorrect Email or Password")
    return tokens.Token(access_token=access_token)