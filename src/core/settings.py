from pathlib import Path
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

path_to_env_file = Path(__file__).parent.parent.parent / ".env"


class BaseEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=path_to_env_file, env_file_encoding="utf-8", extra="ignore"
    )
    DEBUG: bool | None = False
    PROJECT_NAME: str = "default_bot"
    HOST: str
    PORT: int


class PrivateSettings(BaseEnvSettings):
    ADMIN_CHAT_ID: int


class BotSettings(BaseEnvSettings):
    BOT_URL: str
    BOT_TOKEN: str


class DatabaseSettings(BaseEnvSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def db_uri(self) -> str:
        postgres_dns = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
        return str(postgres_dns)


class YooCassaSettings(BaseEnvSettings):
    SHOP_ID: str
    SECRET_KEY: str
    NOTIFICATION_URL: str


class Settings(BotSettings, PrivateSettings, DatabaseSettings, YooCassaSettings):
    pass


settings = Settings()
