import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "dev").lower()
    PROJECT_NAME: str = "Finance Dashboard API"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
    CORS_ALLOW_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
        if origin.strip()
    ]
    EXTERNAL_API_BASE_URL: str = os.getenv(
        "EXTERNAL_API_BASE_URL", "https://api.exchangerate.host")
    EXTERNAL_API_PATH: str = os.getenv("EXTERNAL_API_PATH", "/latest?base=USD")
    EXTERNAL_API_TIMEOUT_SECONDS: float = float(
        os.getenv("EXTERNAL_API_TIMEOUT_SECONDS", "10"))

    def __init__(self) -> None:
        if not self.SECRET_KEY:
            if self.APP_ENV == "prod":
                raise ValueError("SECRET_KEY must be set in production")
            self.SECRET_KEY = "dev-insecure-secret-key-change-me"
        if self.APP_ENV == "prod" and not self.CORS_ALLOW_ORIGINS:
            raise ValueError(
                "CORS_ALLOW_ORIGINS must be configured in production")


settings = Settings()
