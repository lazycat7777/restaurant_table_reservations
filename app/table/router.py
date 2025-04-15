from fastapi import APIRouter
from app.table.dao import TableDAO
from app.table.schemas import TTableAdd


router = APIRouter(prefix="/tables", tags=["Столики"])


@router.get("/", summary="Вернуть список всех столиков")
async def get_all_tables():
    """
    Возвращает список всех столиков.
    """
    return await TableDAO.find_all()


@router.post("/", summary="Добавить новый столик")
async def add_table(table: TTableAdd) -> dict:
    """
    Добавляет новый столик.
    """
    res = await TableDAO.add(**table.model_dump())
    if res:
        return {"message": "Столик добавлен!", "table": table}
    else:
        return {"message": "Произошла ошибка при добавлении столика!"}


@router.delete("/{id}", summary="Удалить столик по ID")
async def delete_table(table_id: int) -> dict:
    """
    Удаляет столик по ID.
    """
    res = await TableDAO.delete(id=table_id)
    if res:
        return {"message": "Столик удален!", "table_id": table_id}
    else:
        return {"message": "Произошла ошибка при удалении столика!"}