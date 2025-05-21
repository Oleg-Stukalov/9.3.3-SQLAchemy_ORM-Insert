import asyncio
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Text, func
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

async def create_user(
    engine: AsyncEngine,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
):
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name
    )
    ###async with AsyncSession(engine) as session:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        session.add(user)
        await session.commit()
        print(user.created_at)

async def main():
    engine = create_async_engine(
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False,
    )

    # Удаление предыдущей версии базы
    # и создание таблиц заново
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    # Создание первого пользователя
    await create_user(
        engine,
        telegram_id=12345,
        first_name="Linus",
        last_name="Torvalds"
    )
    # Сделаем небольшую паузу, чтобы были разные отметки времени
    await asyncio.sleep(1)
    # Создание второго пользователя (без фамилии)
    await create_user(
        engine,
        telegram_id=98765,
        first_name="Jack",
    )

# Точка входа
if __name__ == '__main__':
    asyncio.run(main())