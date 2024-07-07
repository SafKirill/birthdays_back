from typing import Generator

import settings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

#Создание движка для работы с БД(асинх)
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

#Создание сессии работы с БД
asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db() -> Generator:
    try:
        session: AsyncSession = asyncSession()
        yield session
    finally:
        await session.close()
