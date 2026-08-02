from pydantic import BaseModel, EmailStr

from common.validation.field_type_alias import Address
from employee.application.validator.model_validator import EmployeeModelValidator

validator = EmployeeModelValidator


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    manager_id: int | None = None
    department: str | None = None
    role: str | None = None
    salary: float | None = None
    address: Address | None = None
    phone_number: str | None = None
