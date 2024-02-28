from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

DB_USER = settings.POSTGRES_USER
DB_PASSWORD = settings.POSTGRES_PASSWORD
DB_NAME = settings.POSTGRES_DB
DB_HOST = settings.POSTGRES_HOST
async_engine: AsyncEngine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")

Session = async_sessionmaker(async_engine, class_=AsyncSession)


async def get_session():

    @asynccontextmanager
    async def wrapped() -> AsyncSession:
        async with Session() as async_session:
            yield async_session

    return wrapped
