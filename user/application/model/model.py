from pydantic import BaseModel, ConfigDict, EmailStr

from common.validation.field_type_alias import password
from user.application.validator.model_validator import UserModelValidator

validator = UserModelValidator()


class UserRequest(BaseModel):
    email: EmailStr
    password: password
    employee_id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr


class CurrentUser(BaseModel):
    id: int
    email: str
    employee_id: int
