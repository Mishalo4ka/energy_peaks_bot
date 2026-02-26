from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str | None]


class EnergyRecord(Base):
    __tablename__ = "energy_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    energy: Mapped[int]
    concentration: Mapped[int]
    activity: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("User")
