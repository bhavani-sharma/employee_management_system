from fastapi import APIRouter, Depends, HTTPException, status, Query
# from sqlalchemy.ext.asyncio import AsyncSession
from application.services.emp_service.employee_service import CreateEmployee
from math import ceil
from infrastructure.dependencies import get_employee_service
from common.exceptions.exceptions import EmployeeAlreadyExistsError, EmployeeNotFoundError
from infrastructure.schemas.user_schema import Users
from application.models.employees import EmployeeCreate, EmployeeResponse, EmployeeUpdate, PaginatedEmployees
from application.services import auth

router = APIRouter(prefix="/employees", tags=["employees"])
#create employee
@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_emp(
    emp: EmployeeCreate,
    # db: Session = Depends(get_db),
    service: CreateEmployee = Depends(get_employee_service),
    current_user: Users = Depends(auth.get_current_user),
):
    try:
        return service.create_employee(emp, current_user)
    except EmployeeAlreadyExistsError as err:
        raise HTTPException(status_code=404, detail=str(err))



@router.get("", response_model=PaginatedEmployees)
def list_employees(
    page: int = Query(1, ge=1, description="1-indexed page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page (max 100)"),
    # db:Session = Depends(get_db),
    service:CreateEmployee = Depends(get_employee_service),
    current_user: Users = Depends(auth.get_current_user),

):
    items, total = service.list_employees(page, page_size, current_user)
    total_pages = ceil(total/page_size) if total else 0
    return PaginatedEmployees(
        items= items,
        total= total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


#search employee
@router.get("/{employee_id}", response_model=EmployeeResponse, responses={404:{"description": "Employee Not Found"}})
def get_employee_by_id(employee_id: str, service: CreateEmployee = Depends(get_employee_service),
    current_user:Users = Depends(auth.get_current_user)):
    try:
        return service.get_employee(employee_id, current_user)
    except EmployeeNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


#update 
@router.put("/{employee_id}", response_model=EmployeeResponse)
def update(
    employee_id: str, 
    payload: EmployeeUpdate,
    service: CreateEmployee = Depends(get_employee_service),
    current_user: Users = Depends(auth.get_current_user)
):
    try:
        return service.update_employee(employee_id,payload, current_user)
    except EmployeeNotFoundError as err:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=str(err))
    

#delte employee
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    employee_id: str,
    # db:Session = Depends(get_db),
    service: CreateEmployee = Depends(get_employee_service),
    current_user: Users = Depends(auth.get_current_user)
):
    try:
        service.delete_employee(employee_id,current_user)
    except EmployeeNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    return None