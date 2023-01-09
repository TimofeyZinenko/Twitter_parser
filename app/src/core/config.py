"""Config required settings."""


from os import path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field, PostgresDsn, RedisDsn, dataclasses
from src.core.logger import LOGGING

load_dotenv()


class Settings(BaseSettings):
    """Configuration settings."""

    api_key: str = Field(..., env="API_KEY")
    api_secret_key: str = Field(..., env="API_SECRET_KEY")
    api_bearer_token: str = Field(..., env="API_BEARER_TOKEN")
    api_access_token: str = Field(..., env="API_ACCESS_TOKEN")
    api_access_token_secret: str = Field(..., env="API_ACCESS_TOKEN_SECRET")
    base_dir = path.dirname(path.dirname(path.abspath(__file__)))

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


@dataclasses.dataclass
class Status:
    one: str = "success"
    zero: str = "failed"


config_settings = Settings()
status = Status()
