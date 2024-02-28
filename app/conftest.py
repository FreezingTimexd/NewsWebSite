import pytest
from alembic.config import Config
from passlib.handlers import bcrypt
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from app.api.users.service import UserService
from app.config import settings
from app.database import get_session
from app.main import app
from httpx import AsyncClient
import app.models as models

DB_USER = settings.POSTGRES_USER
DB_PASSWORD = settings.POSTGRES_PASSWORD
DB_NAME = settings.TEST_POSTGRES_DB
DB_HOST = settings.POSTGRES_HOST

async_engine: AsyncEngine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")

AsyncTestingSessionLocal = async_sessionmaker(
    async_engine,
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
config = Config(file_="alembic.ini")
config.set_main_option("sqlalchemy.url", f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")


@pytest.fixture()
async def client(session):
    async def override_get_session() -> AsyncTestingSessionLocal:
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        app=app, base_url="http://localhost:8080"
    ) as client:
        yield client


@pytest.fixture()
async def user_test(session):
    user = models.User(
        id=1,
        email="test@test.ru",
        username="test",
        password=bcrypt.hash("test"),
        is_admin=0,
    )
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return await UserService(session).find_by_id(user.id)


# @pytest.fixture()
# async def media_test(session):
#     media = models.MediaFile(
#         id=1,
#         filename="test",
#         filepath="test/test",
#     )
#     session.add(media)
#     await session.flush()
#     await session.refresh(media)
#     return await UserService(session).find_by_id(media.id)
