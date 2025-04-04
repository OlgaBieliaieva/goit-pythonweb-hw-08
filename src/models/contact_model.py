from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from src.conf import constants


class Base(DeclarativeBase):
    pass


class Contact_model(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(
        String(constants.NAME_MAX_LENGTH), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(constants.NAME_MAX_LENGTH), nullable=False
    )
    email: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    phone: Mapped[str | None] = mapped_column(String(constants.PHONE_MAX_LENGTH), unique=True, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    additionally: Mapped[str] = mapped_column(String(constants.ADDITIONALLY_MAX_LENGTH), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )