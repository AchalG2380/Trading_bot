from bot.client import BinanceClient
from bot.logging_config import get_logger
from bot.validators import validate_all

logger = get_logger(__name__)


def _normalize(raw: dict) -> dict:
    return {
        "orderId": raw.get("orderId"),
        "status": raw.get("status"),
        "executedQty": raw.get("executedQty"),
        "avgPrice": raw.get("avgPrice"),
    }


def place_market_order(
    client: BinanceClient, symbol: str, side: str, quantity
) -> dict:
    """Validate inputs, place a MARKET order, and return a normalized result dict."""
    symbol, side, order_type, quantity, _ = validate_all(symbol, side, "MARKET", quantity)

    try:
        raw = client.place_order(symbol, side, order_type, quantity)
        result = _normalize(raw)
        logger.info(
            "MARKET order placed successfully — orderId=%s status=%s",
            result["orderId"],
            result["status"],
        )
        return result
    except Exception:
        logger.error("MARKET order failed — symbol=%s side=%s qty=%s", symbol, side, quantity)
        raise


def place_limit_order(
    client: BinanceClient, symbol: str, side: str, quantity, price
) -> dict:
    """Validate inputs, place a LIMIT order, and return a normalized result dict."""
    symbol, side, order_type, quantity, price = validate_all(
        symbol, side, "LIMIT", quantity, price
    )

    try:
        raw = client.place_order(symbol, side, order_type, quantity, price)
        result = _normalize(raw)
        logger.info(
            "LIMIT order placed successfully — orderId=%s status=%s",
            result["orderId"],
            result["status"],
        )
        return result
    except Exception:
        logger.error(
            "LIMIT order failed — symbol=%s side=%s qty=%s price=%s",
            symbol,
            side,
            quantity,
            price,
        )
        raise
