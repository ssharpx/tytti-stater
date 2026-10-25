from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)

from config import StandartLoader, logging


logger = logging.getLogger(__name__)

standart_obj = StandartLoader()


engine = create_async_engine(
    url=standart_obj.get_db_config,
    pool_size=5,
    max_overflow=5,
)

LocalSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
)

@asynccontextmanager
async def get_db():
    
    logger.info(
        "get_db: database session opened"
    )
    
    async with LocalSession as db:
        try:
            yield db
        finally:
            logger.info(
                "get_db: database session closed"
            )


class BaseModel(DeclarativeBase):
    pass



