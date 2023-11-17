from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config.bot_config import config

from .models import Base

db_user = config.postgres_user.get_secret_value()
db_pass = config.postgres_password.get_secret_value()
db_host = config.postgres_host.get_secret_value()
db_name = config.postgres_db.get_secret_value()
DATABASE_URL = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}/{db_name}'


async def get_db_session(database_url: str) -> AsyncSession:
    """Создает сессию для работы с базой данных."""
    engine = create_async_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return AsyncSession(engine, expire_on_commit=False)
