from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declared_attr

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def get_session(cls, async_session: sessionmaker[AsyncSession]) -> AsyncSession:
        return async_session()
    
Base = declarative_base(cls=CustomBase)
