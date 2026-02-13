from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, func, DateTime

from app.database.base import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
