# Binance Futures Testnet Trading Bot

A lightweight Python CLI application that places **Market** and **Limit** orders on the [Binance Futures Testnet (USDT-M)](https://testnet.binancefuture.com). Built with clean separation between the API client layer and the CLI layer, structured logging, and robust input validation.

---

## Prerequisites

- Python 3.10+
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account with API credentials

---

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/trading_bot.git
cd trading_bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy the example env file and fill in your testnet keys
cp .env.example .env
# Edit .env and replace the placeholder values with your real testnet API key and secret
```

---

## Run Examples

```bash
# Market BUY
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01

# Market SELL
python cli.py --symbol BTCUSDT --side SELL --type MARKET --qty 0.01

# Limit BUY
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --qty 0.01 --price 75826

# Limit SELL
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 75826
```

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py          # Package marker
│   ├── client.py            # Binance REST API wrapper (HMAC signing, HTTP calls)
│   ├── orders.py            # Business logic: place_market_order, place_limit_order
│   ├── validators.py        # Input validation before any API call
│   └── logging_config.py   # Logging setup (file + console handlers)
├── cli.py                   # CLI entry point (argparse)
├── logs/
│   └── trading_bot.log      # Log output from testnet orders
├── .env                     # API keys — never committed
├── .env.example             # Placeholder env file — safe to commit
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Assumptions

- **Testnet only** — the base URL is always `https://testnet.binancefuture.com`. No real funds are used.
- **Symbol format** — use `BTCUSDT` (uppercase, no slash). The validator enforces this.
- **Quantity units** — quantity is in base asset units (e.g. BTC for BTCUSDT).
- **LIMIT orders** — `timeInForce` is set to `GTC` (Good Till Cancelled) by default.
- **Direct REST calls** — no third-party Binance SDK; uses `requests` + manual HMAC-SHA256 signing as described in the [Binance Futures API docs](https://binance-docs.github.io/apidocs/futures/en/).
- **Python version** — requires Python 3.10+ for the `float | None` type hint syntax.
