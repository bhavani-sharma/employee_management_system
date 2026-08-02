from fastapi import APIRouter, status
from fastapi_injector import Injected

import user.application.model.model as models
from user.application.model.token import Token
from user.application.service.service.signin_service import SignInService
from user.application.service.service.signup_service import SignUpService

router = APIRouter(prefix="/user", tags=["user"])


# signup
@router.post(
    "/signup", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(
    payload: models.UserRequest,
    service: SignUpService = Injected(SignUpService),  # noqa: B008
):

    return service.signup(payload)


# signin
@router.post("/signin", response_model=Token)
def signin(
    form_data: models.UserLogin,
    service: SignInService = Injected(SignInService),  # noqa: B008
):
    return service.singin(form_data)
