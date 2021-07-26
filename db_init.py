from typing import Type, Any
from sqlalchemy.ext.declarative import declarative_base
from db_session import engine


Base: Any = declarative_base()


def erase_table(table: Type[Base]) -> None:
    """
    Delete and recreate table
    :param table: Type[Base]
    :return: None
    """
    table.__table__.drop(engine)
    Base.metadata.create_all(engine, tables=[table.__table__])


if __name__ == "__main__":
    Base.metadata.create_all(engine)
