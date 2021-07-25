from typing import List, Tuple, Any
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# TODO: add db data from config
engine: Any = create_engine(
    "postgresql+psycopg2://rfipapp:tmppass@localhost/rfipapp")

Base: Any = declarative_base()


class CollectedData(Base):
    """
    collected_data table init
    """
    __tablename__ = 'collected_data'

    id: int = Column(Integer, primary_key=True, nullable=False)
    begin_ip_address: str = Column(String(15))
    end_ip_address: str = Column(String(15))
    total_count: str = Column(String(15))


class Users(Base):
    """
    users table init
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, nullable=False)
    login: str = Column(String(50), unique=True, nullable=False)
    password: str = Column(String(50), nullable=False)
    created_at: DateTime = Column(DateTime(), default=datetime.utcnow,
                                  nullable=False)
    last_request: DateTime = Column(DateTime())


def get_collected_data() -> List[CollectedData]:
    """
    Get all records in get_collected table and return as list of instances
    of CollectedData
    :return: List[CollectedData]
    """
    return session.query(CollectedData).all()


def update_collected_data(data):
    CollectedData.__table__.drop(engine)
    Base.metadata.create_all(engine, tables=[CollectedData.__table__])

    session.bulk_insert_mappings(
        CollectedData,
        [dict(
            begin_ip_address=bia,
            end_ip_address=eia,
            total_count=tc
        ) for bia, eia, tc in data]
    )
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
