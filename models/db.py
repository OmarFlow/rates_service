from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession

from models.models import Base

load_dotenv()

user = getenv('PG_USER')
password = getenv('PG_PASSWORD')
db = getenv('PG_DB')


async def sync_engine() -> AsyncEngine:
    engine = create_async_engine(
        f"postgresql+asyncpg://{user}:{password}@db/{db}",
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine


async def get_session() -> async_sessionmaker[AsyncSession]:
    engine = await sync_engine()
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    return async_session
