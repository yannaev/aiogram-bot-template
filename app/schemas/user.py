from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    telegram_id: int

class User(UserCreate):
    id: int
    created_at: datetime