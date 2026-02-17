from app.models import UserORM
from app.repositories.base import BaseRepository
from app.schemas.user import UserDTO


class UserRepository(BaseRepository):
    model = UserORM
    schema = UserDTO
