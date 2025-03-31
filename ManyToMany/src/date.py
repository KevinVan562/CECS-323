from typing import List
from orm_base import Base
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from WorkSchedule import WorkSchedule
from datetime import datetime

class WorkDate(Base):
    __tablename__ = "dates"
    shiftDate: Mapped[datetime] = mapped_column("shift_date", Date, default=datetime.today(), nullable=False, primary_key=True)
    holidayFlag: Mapped[str] = mapped_column("holiday", String(50), nullable=True)

    employees: Mapped[List["WorkSchedule"]] = relationship("WorkSchedule", back_populates="date", cascade="all, save-update, delete-orphan")

    __table_args__ = (
        {'schema': 'manytomany'}
    )


    def __str__(self):
        return f"Shift Date: {self.shiftDate}, Holiday: {self.holidayFlag}"