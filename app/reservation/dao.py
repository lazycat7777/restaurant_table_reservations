from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_, func, cast, Interval
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.reservation.models import Reservation
from datetime import timedelta


class ReservationDAO(BaseDao):
    model = Reservation

    @classmethod
    async def add_reservation(cls, **values):
        """
        Добавляет новую бронь, если столик доступен.
        """
        async with async_session_maker() as session:
            if not await cls._is_table_available(
                    session,
                    values['table_id'],
                    values['reservation_time'],
                    values['duration_minutes']
            ):
                raise ValueError("Столик забронирован, прошу забронировать другой")


            new_reservation = cls.model(**values)
            session.add(new_reservation)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_reservation

    @classmethod
    async def _is_table_available(cls, session, table_id, reservation_time, duration_minutes):
        """
        Проверяет, доступен ли столик для бронирования.
        """
        end_time = reservation_time + timedelta(minutes=duration_minutes)

        query = select(cls.model).where(
            and_(
                cls.model.table_id == table_id,
                cls.model.reservation_time < end_time,
                (cls.model.reservation_time + cast(func.concat(cls.model.duration_minutes, ' minutes'), Interval)) > reservation_time
            )
        )

        result = await session.execute(query)
        return result.scalar() is None