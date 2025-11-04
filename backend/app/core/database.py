# app/core/database.py
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine: AsyncEngine | None = None
AsyncSessionLocal: sessionmaker | None = None

async def init_db():
    global engine, AsyncSessionLocal
    if engine is None:
        # DATABASE_URL should be async, e.g.:
        # postgresql+asyncpg://user:pass@host:5432/dbname
        # mysql+aiomysql://user:pass@host:3306/dbname
        # sqlite+aiosqlite:///./app.db
        engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

async def close_db():
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None
