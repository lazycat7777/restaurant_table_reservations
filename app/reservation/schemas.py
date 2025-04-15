from datetime import datetime
from pydantic import BaseModel, Field


class RReservationAdd(BaseModel):
    customer_name: str = Field(..., description="Клиент")
    duration_minutes: int = Field(..., description="Время резервирования")
    reservation_time: datetime
    table_id: int = Field(..., description="id столика")