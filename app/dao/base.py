from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.database import async_session_maker
from sqlalchemy import delete as sqlalchemy_delete


class BaseDao:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Получает все записи, соответствующие фильтрам.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **value):
        """
        Добавляет новую запись в базу данных.
        """
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**value)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        """
        Удаляет записи из базы данных.
        Если delete_all=True, удаляет все записи модели.
        """
        if not delete_all and not filter_by:
            raise ValueError("Укажите минимум один параметр для удаления")

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount