from typing import Optional, List, Tuple
import application.models.employees as employees
import infrastructure.schemas.employee_schema as emp_schema




accepted_roles = ["HR", "Manager", "Admin"]
class Employee_repository:
    def __init__(self,db):
        self.db = db

    def get_by_id(self, emp_id:str)->Optional[emp_schema.Employee]:
        return self.db.query(emp_schema.Employee).filter(emp_schema.Employee.emp_id==emp_id).first()

    def get_by_email(self,email:str)->Optional[emp_schema.Employee]:
        return self.db.query(emp_schema.Employee).filter(emp_schema.Employee.email==email).first()

    def create(self, data:employees.EmployeeCreate)->emp_schema.Employee:
        new_emp = emp_schema.Employee(**data.model_dump())
        if new_emp.role in accepted_roles or new_emp.department =="HR":
            new_emp.is_eligible=True
        else:
            new_emp.is_eligible = False
        self.db.add(new_emp)
        self.db.commit()
        self.db.refresh(new_emp)
        return new_emp
    # employees.EmployeeResponse(
    #         emp_id= new_emp.emp_id,
    #         name= new_emp.name,
    #         salary= f"₹{new_emp.salary:,.2f}",
    #         joining_date=new_emp.joining_date.strftime("%d-%m-%Y"),
    #         date_of_birth= new_emp.date_of_birth.strftime("%d-%m-%Y"),
    #     )

    def update(self, employee: emp_schema.Employee, data:employees.EmployeeUpdate, user_repo)-> emp_schema.Employee:
        if data.role in accepted_roles or data.department == 'HR':
            employee.is_eligible = True
        else:
            employee.is_eligible = False
        
        if not employee.is_eligible and user_repo.get_by_id(employee.emp_id):
            user_repo.delete(employee.email)
        for field, value in data.model_dump().items():
            setattr(employee, field, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee


    def delete(self,employee: emp_schema.Employee)->None:
        self.db.delete(employee)
        self.db.commit()

    def get_page(self,page:int, page_size:int)->Tuple[List[emp_schema.Employee],int]:
        total = self.db.query(emp_schema.Employee).count()
        offset = (page - 1)*page_size
        items = self.db.query(emp_schema.Employee).offset(offset).limit(page_size).all()
        return items, total