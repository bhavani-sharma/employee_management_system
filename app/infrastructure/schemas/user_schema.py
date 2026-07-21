from app.common.data.base import Base

from sqlalchemy import ForeignKey, Column, Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

class Users(Base):
    __tablename__="Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique = True)
    password_hashed: Mapped[str] = mapped_column(String, nullable=False)
    emp_id = Column(String, ForeignKey('Employees.emp_id'),unique=True, index = True)
    employee = relationship('Employee', back_populates='user')