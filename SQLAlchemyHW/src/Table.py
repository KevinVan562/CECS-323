from Orm_base import Base
from sqlalchemy import String, TIMESTAMP, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from datetime import datetime

# Schema table
class Schema(Base):
    __tablename__ = 'schemas'
    name: Mapped[str] = mapped_column('name', String(64), nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column('description', String(128), nullable=False)
    creation_date: Mapped[datetime] = mapped_column('creation_date', TIMESTAMP, default=datetime.utcnow, nullable=False)

    @validates('description')
    def validate_description(self, key, description: str):
        if len(description) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        elif len(description) > 128:
            raise ValueError("Description must be at most 128 characters long.")
        return description

    @validates('creation_date')
    def validate_creation_date(self, key, creation_date: datetime):
        earliest_date = datetime(1960, 1, 1).date()
        today = datetime.today().date()

        if creation_date.date() < earliest_date:
            raise ValueError("Creation date cannot be before the earliest date.")
        elif creation_date.date() > today:
            raise ValueError("Creation date cannot be after today.")
        return creation_date

    def __init__(self, name: str, description: str, creation_date: datetime = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.creation_date = creation_date or datetime.utcnow()

    def __str__(self):
        return f"Schema name: {self.name}, Schema description: {self.description}, Schema creation date: {self.creation_date}"

# Schema Objects table
class SchemaObject(Base):
    __tablename__ = 'schema_objects'
    schema_name: Mapped[str] = mapped_column('schema_name', String(64), ForeignKey('schemas.name'), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column('name', String(64), nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column('description', String(128), nullable=False)
    creation_date: Mapped[datetime] = mapped_column('creation_date', TIMESTAMP, default=datetime.utcnow, nullable=False)

    @validates('creation_date')
    def validate_creation_date(self, key, creation_date: datetime):
        earliest_date = datetime(1960, 1, 1).date()
        today = datetime.today().date()

        if creation_date.date() < earliest_date:
            raise ValueError("Creation date cannot be before the earliest date.")
        elif creation_date.date() > today:
            raise ValueError("Creation date cannot be after today.")
        return creation_date

    def __init__(self, schema_name: str, name: str, description: str, creation_date: datetime = None, **kwargs):
        super().__init__(**kwargs)
        self.schema_name = schema_name
        self.name = name
        self.description = description
        self.creation_date = creation_date or datetime.utcnow()

    def __str__(self):
        return f"Schema Object Schema name: {self.schema_name}, Schema Object name: {self.name}, Schema Object description: {self.description}, Schema Object creation date: {self.creation_date}"