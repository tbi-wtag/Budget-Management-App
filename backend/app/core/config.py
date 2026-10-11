from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import APP_ENV_DEVELOPMENT, APP_TIMEZONE

class BaseConfigSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

class DatabaseSettings(BaseConfigSettings):

    user: str = Field(..., alias="POSTGRES_USER")
    password: str = Field(..., alias="POSTGRES_PASSWORD")
    name: str = Field(..., alias="POSTGRES_DB")
    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(..., alias="POSTGRES_PORT")

    @computed_field
    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @computed_field
    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class Settings(BaseConfigSettings):

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()