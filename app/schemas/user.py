from datetime import datetime

from app.schemas.base import BaseSchema


class UserCreateDTO(BaseSchema):
    telegram_id: int
    referrer_telegram_id: int | None = None


class UserUpdateDTO(BaseSchema):
    is_blocked: bool | None = None
    referrer_telegram_id: int | None = None


class UserDTO(UserCreateDTO):
    id: int
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
