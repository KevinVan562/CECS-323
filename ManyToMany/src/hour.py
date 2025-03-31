from typing import List
from orm_base import Base
from sqlalchemy import String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from WorkSchedule import WorkSchedule

class Hour(Base):
    __tablename__ = "hours"
    shiftName: Mapped[str] = mapped_column("shift_name", String(9), nullable=False, primary_key=True)
    shiftStartHour: Mapped[int] = mapped_column("shift_start_hour", Integer, nullable=False)
    shiftEndHour: Mapped[int] = mapped_column("shift_end_hour", Integer, nullable=False)

    work_schedules: Mapped[List["WorkSchedule"]] = relationship("WorkSchedule", back_populates="hour", cascade="all, save-update, delete-orphan")

    __table_args__ = (
        CheckConstraint('LENGTH(shift_name) >= 4', name='check_shift_name_min_length'),
        CheckConstraint('LENGTH(shift_name) <= 9', name='check_shift_name_max_length'),
        CheckConstraint('shift_start_hour BETWEEN 0 AND 23', name='check_shift_start_hour'),
        CheckConstraint('shift_end_hour BETWEEN 0 AND 23', name='check_shift_end_hour'),
        {'schema': 'manytomany'}
    )

    def __str__(self):
        return f"Shift Name: {self.shiftName}, Start Hour: {self.shiftStartHour}, End Hour: {self.shiftEndHour}"