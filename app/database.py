from typing import Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import mapped_column, declared_attr, DeclarativeBase
from app.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"