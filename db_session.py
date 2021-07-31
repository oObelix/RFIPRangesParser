from sqlalchemy.future import Engine
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

config: Config = Config()
engine: Engine = create_engine(config.db_server_dsn)
session: Session = sessionmaker(bind=engine)()
