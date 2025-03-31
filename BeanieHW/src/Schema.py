from beanie import Document, Link
from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional

class Schema(Document):
    name: str = Field(..., max_length=64)
    description: str = Field(..., min_length=10, max_length=128)
    creation_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'schemas'

    @field_validator('creation_date', mode='before')
    def validate_creation_date(cls, creation_date):
        earliest_date = datetime(1960, 1, 1)
        today = datetime.today()

        if creation_date < earliest_date:
            raise ValueError('Creation date cannot be before 1960')
        elif creation_date > today:
            raise ValueError('Creation date cannot be in the future')
        return creation_date

    def __str__(self):
        return f'Schema name: {self.name} description: {self.description} creation_date: {self.creation_date}'

class SchemaObject(Document):
    schema: Link[Schema]
    name: str = Field(..., max_length=64)
    description: str = Field(..., min_length=10, max_length=128)
    creation_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "schema_objects"

    @field_validator('creation_date', mode='before')
    def validate_creation_date(cls, creation_date):
        earliest_date = datetime(1960, 1, 1)
        today = datetime.today()

        if creation_date < earliest_date:
            raise ValueError("Creation date cannot be before 1960")
        if creation_date > today:
            raise ValueError("Creation date cannot be in the future")
        return creation_date

    def __str__(self):
        if self.schema:
            schema_name = self.schema.name
        else:
            schema_name = "No Schema"
        return f'Schema_name: {schema_name} schema object name: {self.name} creation_date: {self.creation_date}'
