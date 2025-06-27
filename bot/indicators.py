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
    """Detecta un pivote en 'V' del RSI considerando Volumen y MACD."""

    def __init__(
        self,
        period: int = 14,
        oversold: int = 30,
        delta: float = 5.0,
        volume_window: int = 5,
    ) -> None:
        self.period = period
        self.oversold = oversold
        self.delta = delta
        self.volume_window = volume_window

    def compute(self, data: pd.DataFrame) -> Dict[str, Any]:
        rsi = talib.RSI(data['close'], timeperiod=self.period)
        if len(rsi) < max(3, self.volume_window):

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
        volume_avg = data['volume'].tail(self.volume_window).mean()
        volume_cond = data['volume'].iloc[-1] > volume_avg

        macd, signal, _ = talib.MACD(
            data['close'], fastperiod=12, slowperiod=26, signalperiod=9
        )
        macd_cond = macd.iloc[-1] > signal.iloc[-1]

        pivot_v = pivot and volume_cond and macd_cond

        return {
            "rsi_pivot_v": pivot_v,
            "rsi": rsi.iloc[-1],
            "volume_avg": volume_avg,
            "macd": macd.iloc[-1],
        }

        return {"rsi_pivot_v": pivot, "rsi": rsi.iloc[-1]}

