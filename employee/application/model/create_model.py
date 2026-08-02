from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from common.validation.field_type_alias import (
    Address,
    DateOfBirth,
    JoiningDate,
    PanNumber,
    PhoneNumber,
)
from employee.application.model.model_enum import (
    Currency,
    Department,
    Genders,
    Roles,
)
from employee.application.validator.model_validator import EmployeeModelValidator

validator = EmployeeModelValidator()


class EmployeeCreate(BaseModel):
    name: str = Field(..., description="Employee full name", max_length=30)
    email: EmailStr = Field(..., description="Valid email address")

    phone_number: PhoneNumber = Field(
        ..., description="Valid phone number", examples=["9912345678"]
    )

    department: Department = Field(..., description="Department name")
    role: Roles = Field(..., description="Job role")

    joining_date: JoiningDate = Field(
        ..., description="Joining date in YYYY-MM-DD format"
    )

    currency: Currency = Field(..., description="Currency of salary", examples=["INR"])

    salary: float = Field(
        gt=9999,
        description="Enter salary in Rupees",
        examples=[10000],
    )

    date_of_birth: DateOfBirth = Field(
        ...,
        description="Date of birth in YYYY-MM-DD format",
        examples=["2008-01-01"],
    )

    gender: Genders = Field(..., description="Your gender")
    blood_group: str = Field(..., description="Blood group", examples=["A+"])

    manager_id: int | None = Field(
        None,
        description="If no manager, replace with {null}",
    )

    address: Address = Field(
        ...,
        description="Permanent address",
    )

    pan_number: PanNumber = Field(
        ...,
        examples=["ABCDE1234F"],
    )

    emergency_contact_name: str = Field(..., max_length=30)

    emergency_contact_number: PhoneNumber = Field(
        ...,
        examples=["9876543210"],
    )


class EmployeeResponse(EmployeeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    created_by_employee_id: int
    last_modified_at: datetime
    last_modified_by_employee_id: int
