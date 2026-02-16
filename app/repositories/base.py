from pydantic import BaseModel
from sqlalchemy import insert

class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def create(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)

