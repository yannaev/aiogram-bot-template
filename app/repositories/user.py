from app.models import UserOrm
from app.repositories.base import BaseRepository
from app.schemas.user import User, UserCreate


class UserRepository(BaseRepository):
    model = UserOrm
    schema = User
