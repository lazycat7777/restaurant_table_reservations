from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk
from sqlalchemy import func, ForeignKey, DateTime
from datetime import datetime


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int_pk]
    customer_name: Mapped[str_uniq]
    reservation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    duration_minutes: Mapped[int]
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    table: Mapped["Table"] = relationship("Table", back_populates="reservation")



