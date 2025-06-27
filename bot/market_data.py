from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class MarketDataProvider(ABC):
    """Abstract base for market data providers."""

    @abstractmethod
    def fetch_ohlc(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        """Fetch OHLC data for a symbol."""
        raise NotImplementedError


class BinanceFuturesProvider(MarketDataProvider):
    """Fetch data from Binance Futures."""

    def __init__(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        # Here you would initialize the actual Binance client

    def fetch_ohlc(self, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
        """Placeholder method for fetching market data."""
        # Real implementation would call Binance API
        raise NotImplementedError("Binance API integration is required")
