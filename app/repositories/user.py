from app.models import UserOrm
from app.repositories.base import BaseRepository
from app.schemas.user import UserDTO


class UserRepository(BaseRepository):
    model = UserOrm
    schema = UserDTO
