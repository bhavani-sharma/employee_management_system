from typing import Optional
from sqlalchemy.orm import Session
import infrastructure.schemas.user_schema as users
from application.services.auth import hash_password


class User_repository:
    def __init__(self, db: Session):
        self.db = db 

    def get_by_email(self, email:str)->Optional[users.Users]:
        return self.db.query(users.Users).filter(users.Users.email == email).first()


    def get_by_id(self, emp_id:str)->Optional[users.Users]:
        return self.db.query(users.Users).filter(users.Users.emp_id == emp_id).first()

    def create(self, email:str, hashed_password:str, employee_id:str)->users.Users:
        new_user = users.Users(email=email, password_hashed=hash_password(hashed_password), emp_id=employee_id)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def delete(self, email:str)->None:
        user = self.get_by_email(email)
        self.db.delete(user)
        self.db.commit()
