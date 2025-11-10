"""Utility helpers for interacting with the CoinGecko API."""
from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from app.core.settings import settings


class CoinGeckoClient:
    """A small async client responsible for interacting with the CoinGecko API."""

    def __init__(
        self,
        *,
        api_base: str | None = None,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self._api_base = api_base or settings.coingecko_api_base
        self._api_key = api_key or settings.coingecko_api_key
        self._timeout = timeout or settings.request_timeout
        self._client = httpx.AsyncClient(
            base_url=self._api_base,
            timeout=self._timeout,
            headers={"x-cg-pro-api-key": self._api_key},
        )

    async def close(self) -> None:
        """Close the underlying HTTP client."""

        await self._client.aclose()

    async def get(self, path: str, **params: Any) -> Dict[str, Any]:
        """Perform a GET request against the CoinGecko API."""

        response = await self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    async def fetch_global_data(self) -> Dict[str, Any]:
        """Fetch aggregated market statistics."""

        payload = await self.get("/global")
        return payload.get("data", payload)

    async def fetch_market_overview(
        self,
        *,
        vs_currency: str = "usd",
        per_page: int = 10,
    ) -> list[Dict[str, Any]]:
        """Fetch market data for the top cryptocurrencies by market cap."""

        payload = await self.get(
            "/coins/markets",
            vs_currency=vs_currency,
            order="market_cap_desc",
            per_page=per_page,
            page=1,
            sparkline="false",
            price_change_percentage="1h,24h,7d",
        )
        return payload

    async def fetch_coin_details(self, coin_id: str) -> Optional[Dict[str, Any]]:
        """Fetch detailed information for a specific cryptocurrency."""

        if not coin_id:
            return None

        try:
            return await self.get(
                f"/coins/{coin_id}",
                localization="false",
                tickers="false",
                community_data="false",
                developer_data="false",
                sparkline="false",
            )
        except httpx.HTTPStatusError as exc:  # pragma: no cover - FastAPI handles errors
            if exc.response.status_code == 404:
                return None
            raise


async def get_client() -> CoinGeckoClient:
    """FastAPI dependency that yields a CoinGecko client."""

    client = CoinGeckoClient()
    try:
        yield client
    finally:
        await client.close()
