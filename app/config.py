from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
