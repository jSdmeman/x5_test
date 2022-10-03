from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import PG_USER, PG_PASS, PG_HOST, PG_NAME


SYNC_DATABASE_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}/{PG_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{PG_NAME}"

sync_engine = create_engine(SYNC_DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL)

SessionLocal = sessionmaker(
    bind = async_engine,
    autocommit = False,
    autoflush = False,
    expire_on_commit = False,
    class_ = AsyncSession
)

Base = declarative_base()
