from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import os


@dataclass
class Config:
    """Configuration values loaded from .env file."""

    binance_api_key: str
    binance_secret: str
    telegram_token: str
    telegram_chat_id: str
    db_uri: str
    symbols: List[str]
    mode: str = "paper"  # or 'live'
    log_level: str = "INFO"
    allowed_sides: str = "both"  # 'long', 'short', or 'both'


def load_config(env_path: Path = Path(".env")) -> Config:
    """Load environment variables from .env file."""
    load_dotenv(dotenv_path=env_path)

    symbols = os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")

    return Config(
        binance_api_key=os.getenv("BINANCE_API_KEY", ""),
        binance_secret=os.getenv("BINANCE_SECRET", ""),
        telegram_token=os.getenv("TELEGRAM_TOKEN", ""),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        db_uri=os.getenv("DB_URI", "postgresql://user:pass@localhost:5432/bot"),
        symbols=symbols,
        mode=os.getenv("MODE", "paper"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        allowed_sides=os.getenv("ALLOWED_SIDES", "both"),
    )
