"""Entry point for the Crypto Analytics FastAPI application."""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.settings import settings
from app.services.coingecko import CoinGeckoClient, get_client

app = FastAPI(
    title="Crypto Analytics",
    description=(
        "Sitio web interactivo construido con FastAPI para explorar estadísticas "
        "actualizadas del mercado de criptomonedas a través de la API de CoinGecko."
    ),
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    coin_id: Optional[str] = Query(default=None, description="CoinGecko coin identifier"),
    client: CoinGeckoClient = Depends(get_client),
) -> HTMLResponse:
    """Render the main dashboard view."""

    global_data = await client.fetch_global_data()
    market_overview = await client.fetch_market_overview(per_page=12)

    coin_details: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    if coin_id:
        coin_details = await client.fetch_coin_details(coin_id)
        if coin_details is None:
            error_message = "La criptomoneda solicitada no fue encontrada. Verifica el identificador en CoinGecko."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "global_data": global_data,
            "market_overview": market_overview,
            "coin_details": coin_details,
            "settings": settings,
            "error_message": error_message,
        },
    )


@app.get("/api/coins/{coin_id}")
async def api_coin_details(
    coin_id: str,
    client: CoinGeckoClient = Depends(get_client),
) -> Dict[str, Any]:
    """Return JSON metadata for a specific cryptocurrency."""

    coin_details = await client.fetch_coin_details(coin_id)
    if coin_details is None:
        raise HTTPException(status_code=404, detail="La criptomoneda solicitada no fue encontrada.")
    return coin_details


@app.get("/api/global")
async def api_global_market(
    client: CoinGeckoClient = Depends(get_client),
) -> Dict[str, Any]:
    """Return general statistics for the global market."""

    return await client.fetch_global_data()


@app.get("/health")
async def healthcheck() -> Dict[str, str]:
    """Health-check endpoint for monitoring."""

    return {"status": "ok"}
