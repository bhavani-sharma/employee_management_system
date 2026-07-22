from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from typing import Optional, List
from datetime import date, datetime
from fastapi import HTTPException, status

class EmployeeBase(BaseModel):
    emp_id: str = Field(
        ...,
        pattern=r"^I-\d+$",
        description="Employee ID in the format I-<number>"
    )
    name: str = Field(..., description="Employee full name")
    department: str = Field(..., description="Department name")
    role: str = Field(..., description="Job role")
    salary: float = Field(
        ...,
        description="Enter salary in Dollars"
    )
    manager_id: Optional[str] = Field(None, description="Manager employee ID, if applicable")
    email: EmailStr = Field(..., description="Valid email address")
    phone_number: str = Field(
        ...,
        description="Valid phone number"
    )
    joining_date: Optional[date] = Field(None, description="Joining date in YYYY-MM-DD format")
    date_of_birth: Optional[date] = Field(None, description="Date of birth in YYYY-MM-DD format")
    blood_group: str = Field(..., description="Blood group")
    address: str = Field(..., description="Permanent address")
    pan_number: str 
    emergency_contact_number:str
    emergency_contact_name: str
    @field_validator("joining_date", "date_of_birth", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            value = value.strip()
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST, 
                    detail = "Date must be in YYYY-MM-DD format only"
                )
        return value


class EmployeeCreate(EmployeeBase):
    emp_id: str = Field(
        ...,
        pattern=r"^I-[0-9][0-9][0-9]$",
        description="Employee ID in the format I-<number>",
        example="I-001"
    )
    name: str = Field(..., description="Employee full name")
    department: str = Field(..., description="Department name")
    role: str = Field(..., description="Job role")
    salary: float = Field(
        ...,
        description="Enter salary in Dollars"
    )
    manager_id: Optional[str] = Field(None, description="Manager employee ID, if applicable")
    email: EmailStr = Field(..., description="Valid email address")
    phone_number: str = Field(
        ...,
        description="Valid phone number"
    )
    joining_date: date = Field(..., description="Joining date in YYYY-MM-DD format")
    date_of_birth: date = Field(..., description="Date of birth in YYYY-MM-DD format")
    blood_group: str = Field(..., description="Blood group")
    address: str = Field(..., description="Permanent address")
    pan_number: str
    emergency_contact_number:str
    emergency_contact_name: str

    @field_validator("joining_date", "date_of_birth", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime):
            return value.date()
        val = datetime.strptime(value, "%Y-%m-%d").date()
        if val > date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = "Date cannot be in the future"
            )
        
        if isinstance(value, str):
            value = value.strip()
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST, 
                    detail = "Date must be in YYYY-MM-DD format only"
                )
    #     return value

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    role: Optional[str] = None
    salary: Optional[float] = None
    addres: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    model_config = ConfigDict(from_attributes=True)

    emp_id: str


class PaginatedEmployees(BaseModel):
    items: List[EmployeeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
