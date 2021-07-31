from sqlalchemy.future import Engine
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config: Config = Config()
engine: Engine = create_engine(config.db_server_dsn)
session: sessionmaker = sessionmaker(bind=engine)()
