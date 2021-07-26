from typing import List, Tuple, Any, Iterator, ClassVar
from config import Config
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker

config = Config()
engine: Any = create_engine(config.db_server_dsn)

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

    def get_collected_data(self, session: Any) -> List[ClassVar]:
        """
        Get all records in get_collected table and return as list of instances
        of CollectedData
        :return: List[CollectedData]
        """
        # session: Any = sessionmaker(bind=engine)()
        return session.query(self).all()

    def update_collected_data(self,
                              session: Any,
                              begin_ip_address: List[str],
                              end_ip_address: List[str],
                              total_count: List[str]) -> None:
        """
        Replace all data of update_collected with new data
        :param begin_ip_address: List[str]
        :param end_ip_address: List[str]
        :param total_count: List[str]
        :return: None
        """
        CollectedData.__table__.drop(engine)
        Base.metadata.create_all(engine, tables=[CollectedData.__table__])

        data: Iterator[Tuple[str, str, str]] = \
            zip(begin_ip_address, end_ip_address, total_count)

        # session: Any = sessionmaker(bind=engine)()
        session.bulk_insert_mappings(
            CollectedData,
            [dict(
                begin_ip_address=bia,
                end_ip_address=eia,
                total_count=tc
            ) for bia, eia, tc in data]
        )
        session.commit()


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


if __name__ == "__main__":
    Base.metadata.create_all(engine)
