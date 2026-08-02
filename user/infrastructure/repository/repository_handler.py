from injector import Inject
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.exception.exception import DatabaseOperationError

from user.infrastructure.entity.entity import User
from user.infrastructure.repository.repository import UserRepository


class UserRepositoryHandler(UserRepository):
    def __init__(self, db: Inject[Session]):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, password_hash: str, employee_id: int) -> User:
        new_user = User(
            email=email, password_hashed=password_hash, employee_id=employee_id
        )
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError as exc:
            self.db.rollback()
            raise DatabaseOperationError("Unable to create user account") from exc

    def delete(self, email: str) -> None:
        user = self.get_by_email(email)
        if user is None:
            return
        try:
            self.db.delete(user)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DatabaseOperationError("Unable to delete user account") from exc

    def get_by_employee_id(self, employee_id: int) -> User | None:
        return self.db.query(User).filter(User.employee_id == employee_id).first()
