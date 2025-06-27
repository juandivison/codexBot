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

### RSI Pivot V

El indicador `RSIVPivot` detecta picos en forma de "V" en el RSI y ahora tiene en cuenta el volumen y la tendencia del MACD. Para validar la señal se requiere:

1. El RSI forma una "V" desde zona de sobreventa.
2. El volumen de la vela actual supera la media de las últimas cinco velas.
3. El MACD se encuentra por encima de su línea de señal.

Cuando se cumplen estas condiciones, el bot abre una posición larga utilizando la volatilidad medida con ATR para calcular el stop-loss y el tamaño de la posición. Por defecto arriesga el 10% del capital con apalancamiento configurable.

## Configuration

All parameters are loaded from `.env`. Symbols, logging level and mode can be customized without modifying the code.

Key variables:

- `LEVERAGE`: leverage applied to position sizing.
- `ACCOUNT_BALANCE`: initial account capital used by the risk manager.
