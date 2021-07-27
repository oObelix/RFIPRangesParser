from typing import List, Tuple, Any, Iterator
from sqlalchemy import Column, Integer, String, DateTime, exc
from sqlalchemy.ext.declarative import declarative_base
import datetime


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

        session.query(cls).delete()

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
    Users table init
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, nullable=False)
    login: str = Column(String(50), unique=True, nullable=False)
    password: str = Column(String(50), nullable=False)
    created_at: DateTime = Column(DateTime(),
                                  default=datetime.datetime.utcnow(),
                                  nullable=False)
    last_request: DateTime = Column(DateTime())

    @classmethod
    def data_by_login(cls, session: Any, login: str) -> __name__.Users:
        """
        Users instance founded by user login
        :param session: Any
        :param login: str
        :return: Any
        """
        return session.query(cls).filter_by(login=login).first()

    @classmethod
    def data_by_id(cls, session: Any, user_id: int) -> __name__.Users:
        """
        Users instance founded by user id
        :param session: Any
        :param user_id: str
        :return: Any
        """
        return session.query(cls).get(user_id)

    @classmethod
    def valid(cls, session: Any, login: str, password: str) -> bool:
        """
        Check user exist in Users with current login and password
        :param session: Any
        :param login: str
        :param password: str
        :return: bool
        """
        try:
            result: Users = session.query(cls).filter_by(login=login).first()
            if hasattr(result, 'password'):
                return result.password == password
            else:
                raise exc.SQLAlchemyError()
        except exc.SQLAlchemyError:
            return False

    @classmethod
    def valid_id(cls, session: Any, user_id: int) -> bool:
        """
        Check user exist in Users by user id
        :param session: Any
        :param user_id: int
        :return: bool
        """
        return bool(session.query(cls).get(user_id))

    @classmethod
    def connected(cls, session: Any, user_id: int) -> None:
        """
        Set current datetime for user id in Users
        :param session: Any
        :param user_id: int
        :return: bool
        """
        result: Users = cls.data_by_id(session, user_id)
        if hasattr(result, 'last_request'):
            result.last_request = datetime.datetime.utcnow()
        session.commit()
