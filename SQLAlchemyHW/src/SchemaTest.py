import logging
from configparser import ConfigParser

import pytest
from datetime import datetime, timezone, date
from sqlalchemy.exc import IntegrityError, StatementError, DataError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import TIMESTAMP

from Utilities import get_test_engine
from Orm_base import metadata, Base
from Table import Schema, SchemaObject

@pytest.fixture
def db_session():
    config = ConfigParser()
    config.read("config.ini")
    log_level = eval(config["logging"]["level"])
    logging.basicConfig(level=log_level)
    logging.getLogger("sqlalchemy.engine").setLevel(log_level)
    logging.getLogger("sqlalchemy.pool").setLevel(log_level)
    engine = get_test_engine()
    metadata.drop_all(engine)
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    #Base.metadata.drop_all(engine)

# Schema Table Tests
def test_insert_and_find_row(db_session):
    db_session.add(Schema(name="insert", description="This is a test of insert", creation_date= datetime.today()))
    db_session.commit()

    schema_count = db_session.query(Schema).filter_by(name="insert", description="This is a test of insert").count()
    assert schema_count == 1

def test_wrong_data_type(db_session):
    try:
        schema = Schema(name="insert", description=123)

        db_session.add(schema)
        db_session.commit()
    except Exception as e:
        assert isinstance(e, (TypeError, DataError)), f"Expected TypeError or DataError, got {type(e)}"
        db_session.rollback()


def test_value_too_long(db_session):
    invalid_description = "A" * 129
    try:
        schema = Schema(name="insert", description=invalid_description)
        db_session.add(schema)
        db_session.commit()
    except Exception as e:
        assert isinstance(e, ValueError), f"Expected ValueError or DataError, got {type(e)}"
        db_session.rollback()

def test_delete_and_find_row(db_session):
    db_session.add(Schema(name="insert", description="This is a test of insert", creation_date=datetime.today()))
    db_session.commit()

    schema_deleted = db_session.query(Schema).filter_by(name="insert", description="This is a test of insert").first()
    db_session.delete(schema_deleted)
    db_session.commit()

    schema_deleted = db_session.query(Schema).filter_by(name="insert", description="This is a test of insert").first()
    assert schema_deleted is None

# Schema Objects Table Tests
def test_insert_and_find_schema_object(db_session):
    # First, make sure there is a corresponding Schema row to reference
    schema = Schema(name="test_schema", description="This is a test schema", creation_date=datetime.today())
    db_session.add(schema)
    db_session.commit()

    # Insert a SchemaObject that references the Schema by 'test_schema'
    schema_object = SchemaObject(schema_name="test_schema", name="test_object", description="This is a test object", creation_date=datetime.today())
    db_session.add(schema_object)
    db_session.commit()

    # Verify that the row was inserted
    schema_object_count = db_session.query(SchemaObject).filter_by(schema_name="test_schema", name="test_object").count()
    assert schema_object_count == 1

def test_wrong_data_type_schema_object(db_session):
    schema = Schema(name="test_schema", description="This is a test schema", creation_date=datetime.today())
    db_session.add(schema)
    db_session.commit()

    try:
        schema_object = SchemaObject(schema_name="test_schema", name="test_object", description=123, creation_date=datetime.today())  # Integer instead of string
        db_session.add(schema_object)
        db_session.commit()
    except Exception as e:
        assert isinstance(e, (TypeError, DataError)), f"Expected TypeError or DataError, got {type(e)}"
        db_session.rollback()

def test_value_too_long_schema_object(db_session):
    schema = Schema(name="test_schema", description="This is a test schema", creation_date=datetime.today())
    db_session.add(schema)
    db_session.commit()

    invalid_description = "A" * 129
    try:
        schema_object = SchemaObject(schema_name="test_schema", name="test_object", description=invalid_description, creation_date=datetime.today())
        db_session.add(schema_object)
        db_session.commit()
    except Exception as e:
        assert isinstance(e, DataError), f"Expected DataError, but got {type(e)}"
        db_session.rollback()

def test_delete_and_find_schema_object(db_session):
    schema = Schema(name="test_schema", description="This is a test schema", creation_date=datetime.today())
    db_session.add(schema)
    db_session.commit()

    schema_object = SchemaObject(schema_name="test_schema", name="test_object", description="This is a test object", creation_date=datetime.today())
    db_session.add(schema_object)
    db_session.commit()

    schema_object_to_delete = db_session.query(SchemaObject).filter_by(schema_name="test_schema", name="test_object").first()
    db_session.delete(schema_object_to_delete)
    db_session.commit()

    schema_object_deleted = db_session.query(SchemaObject).filter_by(schema_name="test_schema", name="test_object").first()
    assert schema_object_deleted is None
