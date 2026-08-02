from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.data.base import Base


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hashed: Mapped[str] = mapped_column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey("Employee.id"), unique=True, index=True)
    employee = relationship("Employee", back_populates="user")
