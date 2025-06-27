import logging
from datetime import datetime
from typing import Any, Dict, Optional

from .database import Database
from .telegram_notifier import TelegramNotifier


class OrderManager:
    """Manage orders in paper trading mode."""

    def __init__(self, db: Database, notifier: TelegramNotifier) -> None:
        self.db = db
        self.notifier = notifier
        self.logger = logging.getLogger(self.__class__.__name__)

    def open_order(self, symbol: str, side: str, price: float, indicators: Dict[str, Any]) -> int:
        data = {
            "symbol": symbol,
            "side": side,
            "status": "open",
            "entry_price": price,
            "stop_loss": None,
            "take_profit": None,
            "indicators": indicators,
            "created_at": datetime.utcnow(),
            "closed_at": None,
        }
        order_id = self.db.insert_order(data)
        self.logger.info("Orden abierta %s %s", symbol, side)
        self.notifier.send_message(f"Orden abierta {symbol} {side}")
        return order_id

    def close_order(self, order_id: int, price: float) -> None:
        # Placeholder for updating order status and creating trade record
        self.logger.info("Orden %s cerrada", order_id)
        self.notifier.send_message(f"Orden {order_id} cerrada")
