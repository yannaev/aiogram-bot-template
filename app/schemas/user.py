from datetime import datetime

from app.schemas.base import BaseSchema


class UserCreate(BaseSchema):
    telegram_id: int


class User(UserCreate):
    id: int
    created_at: datetime
