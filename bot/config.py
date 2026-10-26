from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    bot_token: SecretStr
    llm_api_key: SecretStr
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    log_level: str = "INFO"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/terms_of_reference"
    redis_url: str = "redis://localhost:6379/0"
    generation_cost_credits: int = 1
    free_welcome_credits: int = 1
    payment_provider: str = "yookassa"
    yookassa_shop_id: str | None = None
    yookassa_secret_key: SecretStr | None = None
    telegram_payment_provider_token: SecretStr | None = None
    worker_max_jobs: int = 10
    worker_job_timeout_seconds: int = 900

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
