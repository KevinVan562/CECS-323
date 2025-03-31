from sqlalchemy import ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm_base import Base

class WorkSchedule(Base):
    __tablename__ = 'schedules'

    employee: Mapped["Employee"] = relationship(back_populates="dates")
    date: Mapped["WorkDate"] = relationship(back_populates="employees")
    hour: Mapped["Hour"] = relationship(back_populates="work_schedules")

    employeeEmployeeID: Mapped[int] = mapped_column("employees_employee_id", ForeignKey("employees.employee_id"), primary_key=True)
    dateShiftDate: Mapped[Date] = mapped_column("dates_shift_date", ForeignKey("dates.shift_date"), primary_key=True)
    hourShiftName: Mapped[str] = mapped_column("hours_shift_name", ForeignKey("hours.shift_name"))

    __table_args__ = (
        UniqueConstraint("employees_employee_id", "dates_shift_date", name="unique_schedule"),
        {'schema': 'manytomany'}
    )

def __str__(self):
    return f"Employee ID: {self.employeeEmployeeID}, Shift Date: {self.dateShiftDate}, Shift Name: {self.shiftName}"