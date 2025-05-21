import asyncio

from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import CreateTable
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Text, func
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

async def main():
    engine = create_engine(
        url="postgresql+psycopg://superuser:superpassword@127.0.0.1/data",
        echo=False
    )

    # Печатает на экран SQL-запрос для создания таблицы в PostgreSQL
    print(CreateTable(User.__table__).compile(dialect=postgresql.dialect()))

    # Удаление предыдущей версии базы
    # и создание таблиц заново
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    asyncio.run(main())