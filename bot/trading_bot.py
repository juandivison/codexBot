import logging
import threading
import time
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from .config import Config
from .database import Database
from .indicators import Indicator, RSI, EMA, ATR, RSIVPivot
from .market_data import BinanceFuturesProvider
from .order_manager import OrderManager
from .risk_management import RiskManager, RiskParameters
from .telegram_notifier import TelegramNotifier


@dataclass
class SymbolContext:
    symbol: str
    indicators: List[Indicator]


class TradingBot:
    """Main trading bot class."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        self.notifier = TelegramNotifier(config.telegram_token, config.telegram_chat_id)
        self.db = Database(config.db_uri)
        self.db.init_db()

        risk_params = RiskParameters()
        self.risk_manager = RiskManager(risk_params)

        self.market = BinanceFuturesProvider(config.binance_api_key, config.binance_secret)
        self.order_manager = OrderManager(self.db, self.notifier)

        self.symbol_contexts: Dict[str, SymbolContext] = {}
        for sym in config.symbols:
            self.symbol_contexts[sym] = SymbolContext(
                symbol=sym,
                indicators=[RSI(), EMA(), ATR(), RSIVPivot()],
            )

        self.risk_manager.update_account_balance(config.account_balance)

    def start(self) -> None:
        threads = []
        for sym in self.symbol_contexts.keys():
            t = threading.Thread(target=self.run_symbol, args=(sym,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def run_symbol(self, symbol: str) -> None:
        ctx = self.symbol_contexts[symbol]
        while True:
            try:
                data = self.market.fetch_ohlc(symbol, interval="1m", limit=100)
                signals = {}
                for ind in ctx.indicators:
                    signals.update(ind.compute(data))

                if signals.get("rsi_pivot_v"):
                    price = float(data['close'].iloc[-1])
                    atr = signals.get("atr")
                    if atr is None:
                        time.sleep(1)
                        continue

                    stop_loss_distance = atr * 2
                    position_value = self.risk_manager.calculate_position_size(stop_loss_distance)
                    quantity = (position_value * self.config.leverage) / price
                    risk_amount = stop_loss_distance * quantity

                    if self.risk_manager.can_open_position(risk_amount):
                        self.logger.info("Pivote RSI en V detectado en %s", symbol)
                        self.order_manager.open_order(symbol, "long", price, signals)
                time.sleep(1)
            except Exception as exc:  # pylint: disable=broad-except
                self.logger.error("Error en el símbolo %s: %s", symbol, exc)
                self.notifier.send_message(f"Error en el símbolo {symbol}: {exc}")
                time.sleep(5)
