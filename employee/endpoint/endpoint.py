from math import ceil

from fastapi import APIRouter, Depends, status
from fastapi_injector import Injected

from common.auth.get_current_user import get_current_user
from common.context.request_context import RequestContext
from employee.application.model.create_model import (
    EmployeeCreate,
    EmployeeResponse,
)
from employee.application.model.list_model import EmployeeList, EmployeePaginated
from employee.application.model.update_model import EmployeeUpdate
from employee.application.service.service.create_service import (
    CreateService,
)
from employee.application.service.service.delete_service import (
    DeleteService,
)
from employee.application.service.service.retrieve_service import (
    RetrieveService,
)
from employee.application.service.service.update_service import (
    UpdateService,
)

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    emp: EmployeeCreate,
    service: CreateService = Injected(CreateService),  # noqa: B008
):
    current_user = RequestContext.get_current_user()
    return service.create(emp, current_user)


@router.get("", response_model=EmployeePaginated)
def list_employees(
    query: EmployeeList = Depends(),  # noqa: B008
    service: RetrieveService = Injected(RetrieveService),  # noqa: B008
):
    current_user = RequestContext.get_current_user()
    items, total = service.list(
        query=query,
        current_user=current_user,
    )
    return EmployeePaginated(
        items=items,
        total=total,
        page=query.page,
        page_size=query.page_size,
        total_pages=ceil(total / query.page_size) if total else 0,
    )


# search employee
@router.get(
    "/{id}",
    response_model=EmployeeResponse,
    responses={404: {"description": "Employee Not Found"}},
)
def get_employee_by_id(
    id: int,
    service: RetrieveService = Injected(RetrieveService),  # noqa: B008
):
    current_user = RequestContext.get_current_user()
    return service.retrieve(id, current_user)


# update
@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(
    id: int,
    payload: EmployeeUpdate,
    service: UpdateService = Injected(UpdateService),  # noqa: B008
):
    current_user = RequestContext.get_current_user()
    return service.update(id, payload, current_user)


# delete employee
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    id: int,
    service: DeleteService = Injected(DeleteService),  # noqa: B008
):
    current_user = RequestContext.get_current_user()
    service.delete(id, current_user)
