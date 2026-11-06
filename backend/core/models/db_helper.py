from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from typing import Annotated, AsyncGenerator
from core.config import settings

class DBHelper:
    def __init__(self, url: str, echo: bool):
        self.engine: AsyncEngine = create_async_engine(url, echo=echo)
        self.sessionmaker: AsyncSession = async_sessionmaker(
            bind = self.engine,
            autocommit = False,
            autoflush = False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.sessionmaker() as session:
            yield session

db_helper = DBHelper(url=settings.db.url, echo=settings.db.echo)