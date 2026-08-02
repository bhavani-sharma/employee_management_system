from injector import Inject
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.exception.exception import (
    DatabaseOperationError,
    DuplicatePanNumberError,
    EmployeeAlreadyExistsError,
)
from employee.application.model.list_model import EmployeeList, EmployeeSummary
from employee.application.model.update_model import EmployeeUpdate
from employee.infrastructure.entity.entity import Employee
from employee.infrastructure.repository.repository import EmployeeRepository

accepted_roles = ["Admin", "HR", "Manager"]


class EmployeeRepositoryHandler(EmployeeRepository):
    def __init__(self, db: Inject[Session]):
        self.db = db

    def get_by_id(self, id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == id).first()

    def get_by_email(self, email: str) -> Employee | None:
        return self.db.query(Employee).filter(Employee.email == email).first()

    def get_by_phone(self, phone: str):
        return self.db.query(Employee).filter(Employee.phone_number == phone).first()

    def get_by_pan(self, pan: str):
        return self.db.query(Employee).filter(Employee.pan_number == pan).first()

    @staticmethod
    def _translate_integrity_error(exc: IntegrityError, action: str) -> None:
        """Convert known unique-constraint violations into stable API errors."""
        detail = str(exc.orig).lower()
        if "pan" in detail:
            raise DuplicatePanNumberError("PAN number must be unique") from exc
        if "phone" in detail:
            raise EmployeeAlreadyExistsError(
                "Phone number is already registered"
            ) from exc
        if "email" in detail:
            raise EmployeeAlreadyExistsError("Email is already registered") from exc
        raise DatabaseOperationError(f"Unable to {action} employee") from exc

    def create(self, data: Employee) -> Employee:
        if self.get_by_email(data.email):
            raise EmployeeAlreadyExistsError("Email is already registered")

        if self.get_by_phone(data.phone_number):
            raise EmployeeAlreadyExistsError("Phone number is already registered")

        if self.get_by_pan(data.pan_number):
            raise DuplicatePanNumberError("PAN number must be unique")
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)

            return data

        except IntegrityError as exc:
            self.db.rollback()
            self._translate_integrity_error(exc, "create")

    def update(self, employee: Employee, data: EmployeeUpdate) -> Employee:
        checking_mail = self.get_by_email(data.email) if data.email else None

        if checking_mail and checking_mail.id != employee.id:
            raise EmployeeAlreadyExistsError(
                "This email is already being used for someone else"
            )

        checking_phone = (
            self.get_by_phone(data.phone_number) if data.phone_number else None
        )
        if checking_phone and checking_phone.id != employee.id:
            raise EmployeeAlreadyExistsError(
                "This phone number is already being used for someone else"
            )

        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(employee, field, value)
        try:
            self.db.commit()
            self.db.refresh(employee)
            return employee
        except IntegrityError as exc:
            self.db.rollback()
            self._translate_integrity_error(exc, "update")

    def delete(self, employee: Employee) -> None:
        try:
            self.db.delete(employee)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            self._translate_integrity_error(exc, "delete")

    def list(self, query: EmployeeList) -> tuple[list[EmployeeSummary], int]:
        query_db = self.db.query(Employee)
        if query.name:
            query_db = query_db.filter(Employee.name.ilike(f"%{query.name}%"))
        if query.email:
            query_db = query_db.filter(Employee.email.ilike(f"%{query.email}%"))
        if query.department:
            query_db = query_db.filter(
                Employee.department.ilike(f"%{query.department}%")
            )
        if query.manager_id is not None:
            query_db = query_db.filter(Employee.manager_id == query.manager_id)
        total = query_db.count()

        sort_column = getattr(Employee, query.sort_by)
        if query.sort_order == "desc":
            sort_column = sort_column.desc()
        query_db = query_db.order_by(sort_column)

        offset = (query.page - 1) * query.page_size
        items = query_db.offset(offset).limit(query.page_size).all()
        return items, total
