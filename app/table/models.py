from sqlalchemy.orm import Mapped, relationship
from app.database import Base, str_uniq, int_pk


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    seats: Mapped[int]
    location: Mapped[str]
    reservation: Mapped[list["Reservation"]] = relationship("Reservation", back_populates="table")