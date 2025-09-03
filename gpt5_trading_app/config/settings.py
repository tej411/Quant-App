from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    ENV: str = "dev"
    TIMEZONE: str = "Europe/Amsterdam"
    BASE_CURRENCY: str = "EUR"
    STARTING_CAPITAL: float = 50_000.0
    CONFIDENCE_THRESHOLD: float = 0.58
    MAX_POSITION_PCT: float = 0.10
    DAILY_LOSS_LIMIT: float = 0.02
    CIRCUIT_VIX_LEVEL: float = 35.0
    CIRCUIT_SPY_DROP: float = 0.04
    DB_URL: str = "sqlite:///gpt5_trading_app.db"
    DATA_DIR: str = "./data_cache"
    ALPACA_API_KEY: str | None = None
    ALPACA_API_SECRET: str | None = None
    ALPACA_BASE_URL: str | None = "https://paper-api.alpaca.markets"

settings = Settings()
os.makedirs(settings.DATA_DIR, exist_ok=True)
