from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).parent.parent
env_file = f"{BASE_DIR}/core/.env"
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class Database(BaseSettings):
    user: str
    password: str
    host: str
    name: str

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:5432/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:5432/{self.name}"

    # url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3" для локальной разработки
    echo: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_prefix="POSTGRES_POSTS_",
        extra="ignore",
    )


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_prefix="RABBITMQ_",
        extra="ignore",
    )
    user: str
    password: str
    host: str
    port: str = "5672"
    services_vhost: str
    celery_vhost: str


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file, env_prefix="REDIS_RESULT_BACKEND_", extra="allow"
    )
    password: str
    host: str
    port: int = 6379


class CelerySettings(BaseSettings):
    rabbitmq: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()
    broker_url: str = (
        f"amqp://{rabbitmq.user}:{rabbitmq.password}@{rabbitmq.host}:{rabbitmq.port}/{rabbitmq.celery_vhost}"
    )
    result_backend: str = f"redis://:{redis.password}@{redis.host}:{redis.port}/0"

    task_default_queue: str = "default_queue"
    task_default_exchange: str = "default_exchange"
    task_default_routing_key: str = "default_routing_key"
    task_time_limit: int = 60 * 5
    accept_content: list[str] = ["json"]
    task_serializer: str = "json"
    result_serializer: str = "json"
    task_track_started: bool = True
    time_zone: str
    enable_utc: bool = False
    ignore_result: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file, env_prefix="CELERY_", extra="allow"
    )


class RunConfig(BaseSettings):
    host: str = "localhost"
    port: int = 8000


class GunicornConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    timeout: int = 30


class LoggingConfig(BaseSettings):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, extra="allow")
    api_v1_prefix: str = "/api/v1"
    docs_prefix: str = "/posts-service"
    time_zone: str
    jwt_secret: str

    database: Database = Database()
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
