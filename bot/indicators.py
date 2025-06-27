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


class RSIVPivot(Indicator):
    """Detecta un pivote en 'V' del RSI."""

    def __init__(self, period: int = 14, oversold: int = 30, delta: float = 5.0) -> None:
        self.period = period
        self.oversold = oversold
        self.delta = delta

    def compute(self, data: pd.DataFrame) -> Dict[str, Any]:
        rsi = talib.RSI(data['close'], timeperiod=self.period)
        if len(rsi) < 3:
            return {"rsi_pivot_v": False}

        pivot = (
            rsi.iloc[-3] > rsi.iloc[-2] < rsi.iloc[-1]
            and rsi.iloc[-2] < self.oversold
            and rsi.iloc[-1] > rsi.iloc[-2] + self.delta
        )
        return {"rsi_pivot_v": pivot, "rsi": rsi.iloc[-1]}
