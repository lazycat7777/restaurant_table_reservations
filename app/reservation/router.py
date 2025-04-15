from fastapi import APIRouter, HTTPException
from app.reservation.dao import ReservationDAO
from app.reservation.schemas import RReservationAdd


router = APIRouter(prefix="/reservation", tags=["Бронирование"])


@router.get("/", summary="Посмотреть все забронированные столики")
async def get_all_reservation():
    """
    Возвращает список всех бронирований.
    """
    return await ReservationDAO.find_all()


@router.post("/", summary="Добавить новую бронь")
async def add_reservation(reservation: RReservationAdd) -> dict:
    """
    Добавляет новую бронь.
    """
    try:
        await ReservationDAO.add_reservation(**reservation.model_dump())
        return {
            "message": "Бронь добавлена!",
            "reservation": reservation
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Произошла ошибка при добавлении брони.")


@router.delete("/{id}", summary="Удалить бронь по ID")
async def delete_reservation(reservation_id: int) -> dict:
    """
    Удаляет бронь по ID.
    """
    res = await ReservationDAO.delete(id=reservation_id)
    if res:
        return {"message": "Бронь удалена!", "reservation_id": reservation_id}
    else:
        return {"message": "Произошла ошибка при удалении брони!"}