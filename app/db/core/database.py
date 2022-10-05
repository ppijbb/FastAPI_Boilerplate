from asyncio import current_task
from typing import Optional, AsyncIterable
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

db_url = '{db_type}://{username}:{password}@{host}:{port}/{db_name}?charset=utf8mb4'\
             .format(db_type="testdb",
                     username="testuser",
                     password="testpassword",
                     host="hostname",
                     port="dbport",
                     db_name="dbname")

Base = declarative_base()


class Database:
    def __init__(self) -> None:
        self.engine: Optional[Engine] = None
        self._session: Optional[scoped_session] = None

    def connect(self) -> None:
        self.engine = create_engine(url=db_url,
                                    convert_unicode=True,
                                    pool_recycle=30,
                                    isolation_level="REPEATABLE READ",
                                    future=True, # Migration to 2.0 Option
                                    echo=False)
        session_factory = sessionmaker(bind=self.engine)
        self._session = scoped_session(session_factory=session_factory,
                                       scopefunc=current_task)
        Base.metadata.create_all(self.engine)

    def dispose(self) -> None:
        if self.engine is None:
            raise RuntimeError("Database Engine is not created")
        self.engine.dispose()

    def get_session(self) -> scoped_session:
        if self._session is None:
            raise RuntimeError("Not Connected to Database")
        return self._session

    def remove_session(self) -> None:
        if self._session is None:
            raise RuntimeError("Not Connected to Database")
        self._session.remove()

    async def get_db_connection(self) -> Engine:
        assert self.engine is not None
        return self.engine

    async def get_db_session(self) -> AsyncIterable[Session]:
        self._session = Session(bind=self.engine,
                                autoflush=False,
                                autocommit=False)
        try:
            yield self.get_session()
        finally:
            self._session.close()
