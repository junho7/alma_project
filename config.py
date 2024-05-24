from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SENDER_EMAIL: str
    ATTORNEY_EMAIL: str
    SECRET_KEY: str
    DATABASE_URL: str
    SMTP_SERVER_URL: str
    SMTP_SERVER_PORT: int
    SMTP_USERNAME: str
    SMTP_APP_PASSWORD: str

settings = Settings(_env_file=".env")
