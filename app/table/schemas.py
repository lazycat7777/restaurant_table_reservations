from pydantic import BaseModel, Field


class TTableAdd(BaseModel):
    name: str = Field(..., description="Название столика")
    seats: int = Field(..., description="Места, кол-во")
    location: str = Field(..., description="Локация столика")
