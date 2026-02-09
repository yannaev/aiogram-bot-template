from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    admin_ids: list[int]

    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    @property
    def db_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.db_user,
                password=self.db_pass,
                host=self.db_host,
                port=self.db_port,
                path=self.db_name,
            )
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
