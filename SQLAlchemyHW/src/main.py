from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from Table import Schema, SchemaObject
from Utilities import get_test_engine
from Orm_base import Base

def main():
    engine = get_test_engine()
    with engine.connect() as connection:
        connection.execute(text('CREATE SCHEMA IF NOT EXISTS "pytest"'))
        connection.commit()

    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    schema = Schema(name="test", description="test")
    session.add(schema)
    session.commit()
if __name__ == "__main__":
    main()