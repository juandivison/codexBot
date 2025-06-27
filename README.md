# codexBot

A modular trading bot skeleton for Binance Futures (USDT pairs). This project focuses on clean architecture, OOP, and ease of extension. The bot operates in paper trading mode using PostgreSQL to store orders and indicator values.

## Requirements

- Python 3.10+
- pandas
- TA-Lib
- python-telegram-bot
- SQLAlchemy
- python-dotenv
- psycopg2-binary

## Usage

1. Copy `.env.example` to `.env` and fill in your credentials.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the bot: `python main.py`.

## Adding Indicators

Add new indicator classes in `bot/indicators.py` inheriting from `Indicator` and implement the `compute` method.

## Configuration

All parameters are loaded from `.env`. Symbols, logging level and mode can be customized without modifying the code.
