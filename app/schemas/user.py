from datetime import datetime

from app.schemas.base import BaseSchema


class UserCreateDTO(BaseSchema):
    telegram_id: int


class UserDTO(UserCreateDTO):
    id: int
    created_at: datetime
