from configparser import ConfigParser
from sqlalchemy import create_engine, Engine
config = ConfigParser()
config.read('config.ini')

def get_test_engine():
    config = ConfigParser()
    config.read('config.ini')
    userID = str = config['credentials']['userid']
    password = str = config['credentials']['password']
    host: str = config['credentials']['host']
    port = str = config['credentials']['port']
    database = config['credentials']['database']

    db_url: str = f"postgresql+psycopg2://{userID}:{password}@{host}/{database}"
    db_url_display: str = f"postgresql+psycopg2://{userID}:********@{host}:{port}/{database}"
    return create_engine(db_url, pool_size=5, pool_recycle=3600, echo=False)