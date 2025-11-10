# Crypto Analytics Overview

Sitio web construido con **FastAPI** que muestra estadísticas de criptomonedas usando la API de CoinGecko.

## Puesta en Marcha

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visita [http://localhost:8000](http://localhost:8000) para ver el panel.

> Data provided by [CoinGecko](https://www.geckoterminal.com/es).

## Estructura Principal

- `app/main.py`: Punto de entrada de FastAPI.
- `app/services/coingecko.py`: Cliente para la API de CoinGecko.
- `app/templates/index.html`: Plantilla principal del dashboard.
- `app/static/styles.css`: Estilos del panel.
