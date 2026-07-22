from fastapi import Depends
from sqlalchemy.orm import Session

from common.data.database import get_db
from application.services.emp_service.employee_service import CreateEmployee
from application.services.users_service.user_service import UserServices

def get_employee_service(db:Session=Depends(get_db))->CreateEmployee:
    return CreateEmployee(db) 

def get_user_service(db:Session = Depends(get_db))->UserServices:
    return UserServices(db)