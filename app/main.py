from fastapi import FastAPI
from app.table.router import router as table_router
from app.reservation.router import router as reservation_router

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Добро пожаловать в API-сервис бронирования столиков в ресторане!"}


app.include_router(table_router)
app.include_router(reservation_router)