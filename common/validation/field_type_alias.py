from datetime import date
from typing import Annotated

from pydantic import BeforeValidator

from employee.application.validator.model_validator import EmployeeModelValidator
from user.application.validator.model_validator import UserModelValidator

emp_validator = EmployeeModelValidator()
user_validator = UserModelValidator()

PhoneNumber = Annotated[
    str,
    BeforeValidator(emp_validator.validate_phone_number),
]

PanNumber = Annotated[
    str,
    BeforeValidator(emp_validator.validate_pan_number),
]

Address = Annotated[
    str,
    BeforeValidator(emp_validator.validate_address),
]

JoiningDate = Annotated[
    date,
    BeforeValidator(lambda value: emp_validator.validate_date(value)),
]

DateOfBirth = Annotated[
    date,
    BeforeValidator(lambda value: emp_validator.validate_dob(value)),
]

password = Annotated[str, BeforeValidator(user_validator.validate_password_strength)]
