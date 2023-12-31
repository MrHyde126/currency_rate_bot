from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    postgres_user: SecretStr
    postgres_password: SecretStr
    postgres_host: SecretStr
    postgres_db: SecretStr
    emoji: bool = True
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


config = Settings()
