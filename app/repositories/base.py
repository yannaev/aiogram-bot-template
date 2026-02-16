from asyncpg import UniqueViolationError, ForeignKeyViolationError
from pydantic import BaseModel
from sqlalchemy import insert, select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound

from app.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    MultipleObjectsFoundException,
    ObjectInUseException,
)


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

        model = result.scalar_one()
        return self.schema.model_validate(model)

    async def get_filtered(self, *filters, **filter_by):
        query = select(self.model).filter(*filters).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        except MultipleResultsFound:
            raise MultipleObjectsFoundException

        return self.schema.model_validate(model)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)

        try:
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                raise ObjectNotFoundException
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ObjectInUseException from ex
            raise ex

    async def delete_all(self):
        await self.session.execute(delete(self.model))
