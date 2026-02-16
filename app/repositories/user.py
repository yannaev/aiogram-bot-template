from app.models import UserOrm
from app.repositories.base import BaseRepository
from app.schemas.user import User, UserCreate


class UserRepository(BaseRepository):
    model = UserOrm
    schema = User

    async def create_user(self, telegram_id: int) -> User:
        user = UserCreate(
            telegram_id=telegram_id
        )
        return await self.create(data=user)