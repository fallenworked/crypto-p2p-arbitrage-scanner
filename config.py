from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str = "7777777777:YOUR_TELEGRAM_BOT_TOKEN_HERE"
    CHANNEL_ID: int = -1001234567890  # ID вашего приватного канала или чата для сигналов
    REDIS_URL: str = "redis://localhost:6379/0"
    
    MIN_SPREAD_PERCENT: float = 0.3
    SCAN_INTERVAL_SECONDS: int = 4

    class Config:
        env_file = ".env"

settings = Settings()
