import pytest
from beanie import init_beanie
from pydantic import ValidationError
from motor.motor_asyncio import AsyncIOMotorClient

from Schema import Schema, SchemaObject

@pytest.fixture
async def init(event_loop):
    client = AsyncIOMotorClient("mongodb://127.0.0.1:27017/")
    db = client.get_database("BeanieHW")
    await init_beanie(database=db, document_models=[Schema, SchemaObject])
    await Schema.delete_all()
    return client

@pytest.mark.asyncio
async def test_insert_and_find_schema(init):
    new_client = await init
    session = await new_client.start_session()

    schema = Schema(
        name='TestSchema',
        description='Testing Schema description'
    )
    await schema.insert(session=session)
    schemas = await schema.find(Schema.name == 'TestSchema',
                                            Schema.description == 'Testing Schema description').to_list()
    assert len(schemas) == 1

@pytest.mark.asyncio
async def test_wrong_data_type(init):
    try:
        schema = Schema(name="InsertInvalidData", description=123)
        await schema.insert()
    except ValidationError as e:
        assert 'description' in str(e)
    else:
        assert False, "Expected ValidationError, not raised"

@pytest.mark.asyncio
async def test_value_too_long(init):
    invalid_description = "A" * 129
    try:
        schema = Schema(name="insert", description=invalid_description)
        await schema.insert()
    except Exception as e:
        assert isinstance(e, ValueError)


@pytest.mark.asyncio
async def test_delete_and_find_schema(init):
    new_client = await init
    session = await new_client.start_session()

    schema = Schema(name="DeleteAndFind", description="This is a test of DeleteAndFind")
    await schema.insert(session=session)

    found_before_deletion = await Schema.find(
        Schema.name == "DeleteAndFind",
        Schema.description == "This is a test of DeleteAndFind"
    ).to_list()

    assert len(found_before_deletion) == 1

    await schema.delete(session=session)

    found_after_deletion = await Schema.find(
        Schema.name == "DeleteAndFind",
        Schema.description == "This is a test of DeleteAndFind"
    ).to_list()

    assert len(found_after_deletion) == 0


# Test for SchemaObject

@pytest.mark.asyncio
async def test_insert_and_find_schema_object(init):
    new_client = await init
    session = await new_client.start_session()

    await Schema.delete_all(session=session)
    await SchemaObject.delete_all(session=session)

    schema = await Schema(name='TestSchema', description='Test schema description').insert(session=session)

    schema_object = SchemaObject(
        schema=schema,
        name='TestSchemaObject',
        description='Testing SchemaObject description'
    )
    await schema_object.insert(session=session)

    schema_objects = await SchemaObject.find(
        SchemaObject.name == 'TestSchemaObject',
        SchemaObject.description == 'Testing SchemaObject description'
    ).to_list()

    assert len(schema_objects) == 1

@pytest.mark.asyncio
async def test_wrong_data_type_for_schema_object(init):
    try:
        schema_object = SchemaObject(name="InsertInvalidData", description=123)
        await schema_object.insert()
    except ValidationError as e:
        assert 'description' in str(e)
    else:
        assert False, "Expected ValidationError, not raised"

@pytest.mark.asyncio
async def test_value_too_long_for_schema_object(init):
    invalid_description = "A" * 129
    try:
        schema_object = SchemaObject(name="insert", description=invalid_description)
        await schema_object.insert()
    except Exception as e:
        assert isinstance(e, ValueError)

@pytest.mark.asyncio
async def test_delete_and_find_schema_object(init):
    new_client = await init
    session = await new_client.start_session()
    await Schema.delete_all(session=session)
    schema = await Schema(name='TestSchema', description='Test schema description').insert(session=session)
    schema_object = SchemaObject(
        schema=schema,
        name="DeleteAndFind",
        description="This is a test of DeleteAndFind"
    )
    await schema_object.insert(session=session)

    found_before_deletion = await SchemaObject.find(
        SchemaObject.name == "DeleteAndFind",
        SchemaObject.description == "This is a test of DeleteAndFind"
    ).to_list()

    assert len(found_before_deletion) == 1

    await schema_object.delete(session=session)
    await schema.delete(session=session)

    found_after_deletion = await SchemaObject.find(
        SchemaObject.name == "DeleteAndFind",
        SchemaObject.description == "This is a test of DeleteAndFind"
    ).to_list()

    assert len(found_after_deletion) == 0

    found_schema = await Schema.find(Schema.name == "TestSchema").to_list()
    assert len(found_schema) == 0

