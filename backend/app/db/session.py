from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.database.async_url,
    poop_pre_ping = True,
    pool_size=35,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=1800,
)

session_local = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    async with session_local() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()