"""Config required settings."""


from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn

load_dotenv()


class Settings(BaseSettings):
    """Configuration settings."""

    api_key: str = Field(..., env="API_KEY")
    api_secret_key: str = Field(..., env="API_SECRET_KEY")
    api_bearer_token: str = Field(..., env="API_BEARER_TOKEN")
    api_access_token: str = Field(..., env="API_ACCESS_TOKEN")
    api_access_token_secret: str = Field(..., env="API_ACCESS_TOKEN_SECRET")

    project_name: str = Field(..., env="PROJECT_NAME")
    cache_expire_in_seconds = 60 * 5  # 5 минут
    postgres_dsn: PostgresDsn
    redis_dsn: RedisDsn
    logger_config = LOGGING

    class Condig:
        """Set config sources."""

        case_sensitive = False

        env_file = ".env"
        env_file_encoding = "utf-8"
        fields = {
            "postgres_dsn": {
                "env": "POSTGRES_DSN",
            },
            "redis_dsn": {
                "env": "REDIS_DSN",
            },
        }


config_settings = Settings()
