from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession, Session

from .config import Config

URL = Config.DATABASE_URL
engine = create_engine("sqlite:///database2.db", echo=False)
async_engine = create_async_engine("sqlite+aiosqlite:///database.db", echo=False)
#async_engine = AsyncEngine(create_engine(url=URL))

async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

#typeignore recordatorio
async def get_session() -> AsyncSession: # type: ignore
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session