from abc import ABC, abstractmethod
from typing import Any, Dict

import pandas as pd
import talib


class Indicator(ABC):
    """Base class for all indicators."""

    @abstractmethod
    def compute(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Compute indicator values from market data."""
        raise NotImplementedError


class RSI(Indicator):
    """Relative Strength Index indicator."""

    def __init__(self, period: int = 14) -> None:
        self.period = period

    def compute(self, data: pd.DataFrame) -> Dict[str, Any]:
        rsi_values = talib.RSI(data['close'], timeperiod=self.period)
        return {"rsi": rsi_values.iloc[-1]}


class EMA(Indicator):
    """Exponential Moving Average indicator."""

    def __init__(self, period: int = 20, column: str = 'close') -> None:
        self.period = period
        self.column = column

    def compute(self, data: pd.DataFrame) -> Dict[str, Any]:
        ema_values = talib.EMA(data[self.column], timeperiod=self.period)
        return {f"ema_{self.period}": ema_values.iloc[-1]}
