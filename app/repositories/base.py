from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from app.exceptions.exceptions import ObjectAlreadyExistsException


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def create(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)

        try:
            result = await self.session.execute(stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException
            raise ex

        model = result.scalars().one()
        return self.schema.model_validate(model)
