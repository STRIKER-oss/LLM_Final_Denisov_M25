import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.core.config import settings

async def init_db():
    DATABASE_URL = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())
