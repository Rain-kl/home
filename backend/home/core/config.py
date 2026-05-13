from functools import cached_property

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "home-backend"
    app_env: str = "dev"
    host: str = "0.0.0.0"
    port: int = 45600
    log_level: str = "INFO"
    database_url: str = "sqlite:///./data/home.db"
    cors_origins: str = "*"
    session_cookie_name: str = "token"
    session_ttl_seconds: int = 2_592_000
    admin_username: str = "admin"
    admin_password: str = Field(default="admin123", repr=False)
    public_cache_ttl_seconds: int = 30

    @cached_property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
