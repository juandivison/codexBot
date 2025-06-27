import logging

from bot.config import load_config
from bot.logging_config import setup_logging
from bot.trading_bot import TradingBot


def main() -> None:
    config = load_config()
    setup_logging(config.log_level)
    bot = TradingBot(config)
    bot.start()


if __name__ == "__main__":
    main()
