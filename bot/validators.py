class ValidationError(ValueError):
    """Raised when user input fails validation."""
    pass


def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("symbol must be a non-empty string (e.g. BTCUSDT)")
    normalized = symbol.upper().strip()
    if "/" in normalized:
        raise ValidationError(
            f"symbol must not contain '/'. Use BTCUSDT format, not BTC/USDT"
        )
    return normalized


def validate_side(side: str) -> str:
    normalized = side.upper().strip()
    if normalized not in ("BUY", "SELL"):
        raise ValidationError(f"side must be BUY or SELL, got '{side}'")
    return normalized


def validate_order_type(order_type: str) -> str:
    normalized = order_type.upper().strip()
    if normalized not in ("MARKET", "LIMIT"):
        raise ValidationError(f"order type must be MARKET or LIMIT, got '{order_type}'")
    return normalized


def validate_quantity(quantity) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"quantity must be a number, got '{quantity}'")
    if qty <= 0:
        raise ValidationError(f"quantity must be positive (> 0), got {qty}")
    return qty


def validate_price(price, order_type: str) -> float | None:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("price is required for LIMIT orders")
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"price must be a number, got '{price}'")
        if p <= 0:
            raise ValidationError(f"price must be positive (> 0), got {p}")
        return p
    return None


def validate_all(symbol: str, side: str, order_type: str, quantity, price=None):
    """Run all validations and return normalized values."""
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    return symbol, side, order_type, quantity, price
