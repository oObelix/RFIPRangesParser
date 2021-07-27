from typing import Any
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config: Config = Config()
engine: Any = create_engine(config.db_server_dsn)
session: Any = sessionmaker(bind=engine)()
