from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ADMIN_EMAIL_ADDRESS: str
    ATTORNEY_EMAIL_ADDRESS: str
    SECRET_KEY: str
    DATABASE_URL: str
    SMTP_URL: str
    SMTP_PORT: int

    class Config:
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()
