from common.data.base import Base
from sqlalchemy import Column, String, Float, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from infrastructure.schemas.user_schema import Users  # noqa: F401

class Employee(Base):
    __tablename__ = "Employees"

    emp_id: Mapped[str] = mapped_column(String, primary_key=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String)
    department: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[float] = mapped_column(Float)
    manager_id: Mapped[str] = mapped_column(String, nullable = True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    user = relationship('Users', back_populates='employee', cascade="all, delete-orphan")
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False , system_default=date(2008,1,1))
    is_eligible = Column(Boolean, default=False, nullable=False)
    blood_group : Mapped[str] = mapped_column(String, nullable=True)
    address : Mapped[str] = mapped_column(String)
    pan_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    emergency_contact_number: Mapped[str] = mapped_column(String)
    emergency_contact_name: Mapped[str] = mapped_column(String)