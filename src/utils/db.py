from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from src.utils.settings import settings
from sqlalchemy.pool import NullPool

class Base(DeclarativeBase, AsyncAttrs):
    pass

engine = create_async_engine(
    url=settings.DB_CONNECTION,
    poolclass=NullPool,
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    },
)
local_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with local_session() as session:
        try:    
            yield session
        finally:
            await session.close()