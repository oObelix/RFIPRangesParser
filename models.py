from typing import List, Tuple, Any, Iterator
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db_init import erase_table, Base


class CollectedData(Base):
    """
    collected_data table init
    """
    __tablename__ = 'collected_data'

    id: int = Column(Integer, primary_key=True, nullable=False)
    begin_ip_address: str = Column(String(15))
    end_ip_address: str = Column(String(15))
    total_count: str = Column(String(15))

    @classmethod
    def get_collected_data(cls, session: Any) -> List:
        """
        Get all records in get_collected table and return as list of instances
        of CollectedData
        :return: List[CollectedData]
        """
        return session.query(cls).all()

    @classmethod
    def update_collected_data(cls,
                              session: Any,
                              begin_ip_address: List[str],
                              end_ip_address: List[str],
                              total_count: List[str]) -> None:
        """
        Replace all data of update_collected with new data
        :param session: Any
        :param begin_ip_address: List[str]
        :param end_ip_address: List[str]
        :param total_count: List[str]
        :return: None
        """

        erase_table(cls)

        data: Iterator[Tuple[str, str, str]] = \
            zip(begin_ip_address, end_ip_address, total_count)

        session.bulk_insert_mappings(
            cls,
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
