from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Session, declarative_base, sessionmaker


# TODO: add db data from config
engine = create_engine(
    "postgresql+psycopg2://rfipapp:tmppass@localhost/rfipapp")

Base = declarative_base()


class CollectedData(Base):
    __tablename__ = 'collected_data'
    id = Column(Integer, primary_key=True, nullable=False)
    begin_ip_address = Column(String(15))
    end_ip_address = Column(String(15))
    total_count = Column(String(15))


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False)
    last_request = Column(DateTime())


Base.metadata.create_all(engine)


def update_collected_data(data):
    CollectedData.__table__.drop(engine)
    Base.metadata.create_all(engine, tables=[CollectedData.__table__])

    Session = sessionmaker(bind=engine)
    session = Session()

    session.bulk_insert_mappings(
        CollectedData,
        [dict(
            begin_ip_address=bia,
            end_ip_address=eia,
            total_count=tc
        ) for bia, eia, tc in data]
    )
    session.commit()
