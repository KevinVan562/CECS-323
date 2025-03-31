import logging
from configparser import ConfigParser
import pytest
from datetime import datetime, timezone, date
from sqlalchemy.exc import IntegrityError, StatementError, DataError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import TIMESTAMP, inspect
from utilities import get_test_engine
from orm_base import metadata, Base
from employee import Employee
from hour import Hour
from date import WorkDate
from WorkSchedule import WorkSchedule

@pytest.fixture
def db_session():
    config = ConfigParser()
    config.read("config.ini")
    engine = get_test_engine()
    metadata.drop_all(engine)
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    #Base.metadata.drop_all(engine)


def test_tables_created(db_session):
    """Test that the tables are created."""
    inspector = inspect(db_session.bind)

    # List of expected tables
    expected_tables = ['schedules', 'employees', 'dates', 'hours']

    # Fetch the list of tables
    actual_tables = inspector.get_table_names(schema='manytomany')  # Specify the schema if needed

    # Check if all expected tables exist
    for table in expected_tables:
        assert table in actual_tables, f"Table '{table}' not found in the database."


