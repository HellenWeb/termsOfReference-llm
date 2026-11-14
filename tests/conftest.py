"""Общие фикстуры pytest."""
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from unittest.mock import AsyncMock
from bot.infrastructure.db.base import Base
from tests.fixtures.messages import make_callback, make_message
from tests.fixtures.users import make_user


@pytest.fixture
def mock_bot() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.fixture
def fake_user():
    return make_user()


@pytest.fixture
def fake_message() -> AsyncMock:
    return make_message()


@pytest.fixture
def fake_callback() -> AsyncMock:
    return make_callback()
