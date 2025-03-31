from orm_base import Base
from sqlalchemy import Integer, Identity, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from WorkSchedule import WorkSchedule

class Employee(Base):
    __tablename__ = 'employees'
    employeeID: Mapped[int] = mapped_column('employee_id', Integer, Identity(start=1, cycle=True), primary_key=True)
    firstName: Mapped[str] = mapped_column('first_name', String(80), nullable=False)
    lastName: Mapped[str] = mapped_column('last_name', String(80), nullable=False)

    dates: Mapped[List["WorkSchedule"]] = relationship("WorkSchedule", back_populates="employee", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('LENGTH(first_name) >= 4', name='check_first_name_min_length'),
        CheckConstraint('LENGTH(first_name) <= 80', name='check_first_name_max_length'),
        CheckConstraint('LENGTH(last_name) >= 4', name='check_last_name_min_length'),
        CheckConstraint('LENGTH(last_name) <= 80', name='check_last_name_max_length'),
        {'schema': 'manytomany'}
    )

    def __init__(self, firstName: str, lastName: str):
        self.firstName = firstName
        self.lastName = lastName

    def __str__(self):
        return f"Employee ID: {self.employeeID}, First Name: {self.firstName}, Last Name: {self.lastName}"