from sqlalchemy.orm import Session
from ..models.base import Base
from ..config.database import engine

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
