import argparse
import sys

from bot.client import BinanceClient
from bot.logging_config import get_logger
from bot.orders import place_limit_order, place_market_order
from bot.validators import ValidationError

logger = get_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet — place MARKET or LIMIT orders"
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--qty", type=float, required=True, help="Order quantity")
    parser.add_argument("--price", type=float, default=None, help="Limit price (required for LIMIT)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Print order summary before placing
    print("\n── Order Summary ──────────────────────────────")
    print(f"  Symbol     : {args.symbol.upper()}")
    print(f"  Side       : {args.side.upper()}")
    print(f"  Type       : {args.order_type.upper()}")
    print(f"  Quantity   : {args.qty}")
    if args.order_type.upper() == "LIMIT":
        print(f"  Price      : {args.price}")
    print("────────────────────────────────────────────────\n")

    try:
        client = BinanceClient()

        if args.order_type.upper() == "MARKET":
            result = place_market_order(client, args.symbol, args.side, args.qty)
        else:
            result = place_limit_order(client, args.symbol, args.side, args.qty, args.price)

        print("── Order Response ─────────────────────────────")
        print(f"  Order ID     : {result['orderId']}")
        print(f"  Status       : {result['status']}")
        print(f"  Executed Qty : {result['executedQty']}")
        print(f"  Avg Price    : {result['avgPrice']}")
        print("────────────────────────────────────────────────")
        print("\n✅ Order placed successfully\n")

    except ValidationError as exc:
        print(f"\n❌ Order failed: {exc}\n")
        logger.error("Validation error: %s", exc)
        sys.exit(1)

    except EnvironmentError as exc:
        print(f"\n❌ Order failed: {exc}\n")
        sys.exit(1)

    except Exception as exc:
        print(f"\n❌ Order failed: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
