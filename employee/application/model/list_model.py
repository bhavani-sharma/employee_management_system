from pydantic import BaseModel, ConfigDict, EmailStr, Field

from employee.application.model.model_enum import EmployeeSortField, SortOrder


class EmployeeSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    department: str
    role: str
    manager_id: int | None


class EmployeePaginated(BaseModel):
    items: list[EmployeeSummary]
    total: int
    page: int
    page_size: int
    total_pages: int


class EmployeeList(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1)

    name: str | None = None
    email: str | None = None
    department: str | None = None
    manager_id: int | None = None

    sort_by: EmployeeSortField = EmployeeSortField.id
    sort_order: SortOrder = SortOrder.asc
