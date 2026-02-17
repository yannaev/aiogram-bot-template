from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, func, DateTime, false

from app.database.base import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    referrer_telegram_id: Mapped[int | None] = mapped_column(BigInteger, index=True)
    is_blocked: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
