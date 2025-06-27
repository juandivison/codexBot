import logging
from typing import Optional

from telegram import Bot
from telegram.error import TelegramError


class TelegramNotifier:
    """Send notifications to Telegram in Spanish."""

    def __init__(self, token: str, chat_id: str) -> None:
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_message(self, message: str) -> None:
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
        except TelegramError as exc:
            self.logger.error("Error al enviar mensaje de Telegram: %s", exc)
