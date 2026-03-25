from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Planify API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./planify.db"

    # JWT
    SECRET_KEY: str = "changethisinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # CLOUDINARY
    CLOUDINARY_CLOUD_NAME: str = "REDACTED"
    CLOUDINARY_API_KEY: str = "REDACTED"
    CLOUDINARY_API_SECRET: str = "REDACTED"

    class Config:
        env_file = ".env"


settings = Settings()