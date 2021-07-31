from typing import List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import Session, Query

Base: declarative_base = declarative_base()


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
    def get_collected_data(cls, session: Session) -> List[Query]:
        """
        Get all records in get_collected table and return as list of instances
        of CollectedData
        :return: List[CollectedData]
        """
        return session.query(cls).all()

    @classmethod
    def update_collected_data(cls,
                              session: Session,
                              begin_ip_address: List[str],
                              end_ip_address: List[str],
                              total_count: List[str]) -> None:
        """
        Replace all data of update_collected with new data
        :param session: Session
        :param begin_ip_address: List[str]
        :param end_ip_address: List[str]
        :param total_count: List[str]
        :return: None
        """
        session.query(cls).delete()

        # https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#usage
        session.bulk_insert_mappings(cls,
                                     [dict(begin_ip_address=bia,
                                           end_ip_address=eia,
                                           total_count=tc)
                                      for bia, eia, tc in zip(begin_ip_address,
                                                              end_ip_address,
                                                              total_count)]
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
    def data_by_login(cls, session: Session, login: str) -> Query:
        """
        Users instance founded by user login
        :param session: Session
        :param login: str
        :return: Query
        """
        return session.query(cls).filter_by(login=login).first()

    @classmethod
    def data_by_id(cls, session: Session, user_id: int) -> Query:
        """
        Users instance founded by user id
        :param session: Session
        :param user_id: str
        :return: Query
        """
        return session.query(cls).get(user_id)

    @classmethod
    def valid(cls, session: Session, login: str, password: str) -> bool:
        """
        Check user exist in Users with current login and password
        :param session: Session
        :param login: str
        :param password: str
        :return: bool
        """
        result: Users = session.query(cls).filter_by(login=login).first()
        if result:
            return result.password == password
        return False

    @classmethod
    def valid_id(cls, session: Session, user_id: int) -> bool:
        """
        Check user exist in Users by user id
        :param session: Session
        :param user_id: int
        :return: bool
        """
        return bool(session.query(cls).get(user_id))

    @classmethod
    def connected(cls, session: Session, user_id: int) -> None:
        """
        Set current datetime for user id in Users
        :param session: Session
        :param user_id: int
        :return: bool
        """
        result: Query = cls.data_by_id(session, user_id)
        if result:
            result.last_request = datetime.datetime.utcnow()
        session.commit()
