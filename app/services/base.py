from app.database.manager import DBManager


class BaseService:
    def __init__(self, db: DBManager) -> None:
        self.db = db
