from datetime import UTC, date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.data.base import Base


class Employee(Base):
    __tablename__ = "Employee"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    department: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(String)
    salary: Mapped[float] = mapped_column(Float)
    user = relationship("User", back_populates="employee", cascade="all, delete-orphan")
    date_of_birth: Mapped[date] = mapped_column(
        Date, nullable=False, default=date(2008, 1, 1)
    )
    manager_id: Mapped[int] = mapped_column(Integer, nullable=True)
    is_eligible = Column(Boolean, default=False, nullable=False)
    blood_group: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String)
    pan_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    emergency_contact_number: Mapped[str] = mapped_column(String)
    emergency_contact_name: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    created_by_employee_id = Column(Integer, nullable=False)
    last_modified_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=datetime.utcnow,
        nullable=False,
    )
    last_modified_by_employee_id = Column(Integer, nullable=False)
