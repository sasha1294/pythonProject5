from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

engin = create_async_engine(url=f'postgresql+asyncpg://postgres:123@localhost:5432/postgres',
                      echo=True)

Session = async_sessionmaker(bind=engin, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def create_base():
    async with engin.begin() as coon:
      #await coon.run_sync(Base.metadata.drop_all)
      await coon.run_sync(Base.metadata.create_all)

def connection(method):
    async def wrapper(*args, **kwargs):
        async with Session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper

