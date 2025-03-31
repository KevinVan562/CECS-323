import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from datetime import datetime
from Schema import Schema, SchemaObject


@pytest.fixture
async def init(event_loop):
    client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
    db = client.get_database("BeanieHW")
    await init_beanie(database=db, document_models=[Schema, SchemaObject])
    return client


@pytest.mark.asyncio
async def test_insert_and_find_schema(init):
    # Await the init fixture to get the client
    client = await init

    # Start a session
    session = await client.start_session()

    try:
        # Create schema without specifying creation_date (let it use default_factory)
        schema = Schema(
            name="Test Schema",
            description="This is a test schema with sufficient length"
        )

        # Insert the document
        await schema.insert(session=session)

        # Store the creation_date for validation
        created_date = schema.creation_date

        # Find the inserted document
        found_schema = await Schema.find_one(Schema.name == "Test Schema")

        # Assertions
        assert found_schema is not None
        assert found_schema.name == "Test Schema"
        assert found_schema.description == "This is a test schema with sufficient length"

        # Verify the creation_date is the same and not in the future
        assert found_schema.creation_date == created_date
        assert found_schema.creation_date <= datetime.today()

        # Clean up
        await found_schema.delete()
    finally:
        await session.end_session()


@pytest.mark.asyncio
async def test_schema_validation(init):
    client = await init
    session = await client.start_session()

    try:
        # Test minimum description length validation
        with pytest.raises(ValueError):
            schema = Schema(
                name="Test",
                description="Too short"  # Should fail min_length=10
            )

        # Test maximum name length validation
        with pytest.raises(ValueError):
            schema = Schema(
                name="T" * 65,  # Should fail max_length=64
                description="This is a valid description"
            )

        # Test successful creation with valid data
        valid_schema = Schema(
            name="Valid Test",
            description="This is a valid description for testing"
        )
        await valid_schema.insert(session=session)

        # Clean up
        await valid_schema.delete()

    finally:
        await session.end_session()
