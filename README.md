<div align="center">

# E-commerce API Prototype

**A small FastAPI project focused on product and order business rules.**

[![CI](https://github.com/fergodoii94/ecommerce-backend-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/fergodoii94/ecommerce-backend-api/actions/workflows/ci-cd.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)

</div>

A small Python/FastAPI learning project for a product catalog and order-submission flow. It currently uses in-memory state so the business rules can be explored without a database.

## What it demonstrates

- `GET /products`: returns the sample catalog.
- `POST /orders`: validates product IDs, rejects duplicate or unknown products, checks stock, calculates the total on the server and decrements stock.
- Pydantic validation for product data and order requests.
- Decimal arithmetic for prices.
- Pytest API tests and Ruff linting in GitHub Actions.

## Engineering decisions

| Decision | Why it was chosen | Trade-off |
|---|---|---|
| Calculate totals on the server | The client sends product IDs only; prices and totals come from the catalog. | Prices are still held in process memory. |
| Use `Decimal` for prices | Avoid binary floating-point rounding in monetary calculations. | API responses serialize decimal values as strings. |
| Validate all product IDs and stock before changing inventory | Unknown or unavailable products are rejected before stock is decremented. | The in-memory implementation is not safe against concurrent orders. |
| Keep catalog and orders in memory | Make the prototype easy to run and inspect without database setup. | State is lost on restart; there are no database transactions or durable order records. |

## Tech stack

- Python 3.11+
- FastAPI
- Pydantic
- Pytest, HTTPX and Ruff

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload
```

OpenAPI documentation: http://127.0.0.1:8000/docs.

## Example requests

List products:

```bash
curl http://127.0.0.1:8000/products
```

Create an order:

```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"product_ids": [1]}'
```

The server calculates the order total from catalog prices; clients cannot submit their own total.

## Quality checks

```bash
ruff check main.py tests
pytest -q
```

## Limitations and next steps

> **Portfolio scope:** This is a prototype, not a production e-commerce backend.

Catalog, stock and orders live in Python memory and are lost when the process restarts. The sample does not provide database transactions, concurrency-safe stock reservation, order persistence, customer accounts, authentication/authorization, payment integration, rate limiting or deployment configuration. Do not use it to process real orders.

Next engineering steps:

1. PostgreSQL persistence with SQLAlchemy and Alembic.
2. Transactional inventory reservation.
3. Customer/order ownership and authentication.
4. Payment-provider integration and idempotency keys.
5. Broader unit and integration test coverage.

---

<div align="center">
  <sub>Part of my Python backend engineering portfolio.</sub>
</div>
