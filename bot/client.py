import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot.logging_config import get_logger

load_dotenv()

logger = get_logger(__name__)


class BinanceAPIException(Exception):
    """Raised when Binance returns an API-level error."""

    def __init__(self, status_code: int, code: int, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(f"[HTTP {status_code}] Binance error {code}: {message}")


class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.base_url = os.getenv(
            "BINANCE_TESTNET_URL", "https://testnet.binancefuture.com"
        )

        if not self.api_key or not self.api_secret:
            raise EnvironmentError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env"
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

    def _sign(self, params: dict) -> dict:
        """Add timestamp and HMAC-SHA256 signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> dict:
        """Send an order to Binance Futures Testnet and return the response dict."""
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        logger.debug(
            "Outgoing order request — symbol=%s side=%s type=%s qty=%s price=%s",
            symbol,
            side,
            order_type,
            quantity,
            price,
        )

        signed_params = self._sign(params)
        url = f"{self.base_url}/fapi/v1/order"

        try:
            response = self.session.post(url, data=signed_params, timeout=10)
        except requests.exceptions.ConnectionError as exc:
            logger.error("Network error — could not reach %s: %s", self.base_url, exc)
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out after 10s")
            raise

        data = response.json()

        if response.status_code != 200:
            code = data.get("code", response.status_code)
            msg = data.get("msg", response.text)
            logger.error(
                "Binance API error — HTTP %s | code=%s | msg=%s",
                response.status_code,
                code,
                msg,
            )
            raise BinanceAPIException(response.status_code, code, msg)

        logger.debug(
            "Order response — orderId=%s status=%s executedQty=%s avgPrice=%s",
            data.get("orderId"),
            data.get("status"),
            data.get("executedQty"),
            data.get("avgPrice"),
        )

        return data
