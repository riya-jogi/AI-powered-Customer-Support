from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI-powered-Customer-Support"
    environment: str = "development"

    database_url: str = "sqlite:///./AI-powered-Customer-Support.db"

    openai_api_key: str
    openai_model: str = "gpt-5.6-luna"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()