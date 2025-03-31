from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

schema = config['schema']['schema name']

metadata_obj = MetaData(schema=schema)

class Base(DeclarativeBase):
    metadata = metadata_obj

metadata = Base.metadata