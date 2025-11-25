from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# Асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Можно поставить True, чтобы видеть SQL запросы в консоли при отладке
    # pool_pre_ping=True,
)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Асинхронная зависимость (Dependency)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()