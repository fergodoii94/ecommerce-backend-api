# E-commerce API Prototype

A small Python/FastAPI learning project for a product catalog and order-submission flow. It currently uses in-memory state so the business rules can be explored without a database.

[![CI](https://github.com/fergodoii94/ecommerce-backend-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/fergodoii94/ecommerce-backend-api/actions/workflows/ci-cd.yml)

## Implemented features

- `GET /products`: returns the sample catalog.
- `POST /orders`: validates product IDs, rejects duplicate or unknown products, checks stock, calculates the total on the server and decrements stock.
- Pydantic validation for product data and order requests.
- Decimal arithmetic for prices.
- Pytest API tests and Ruff linting in GitHub Actions.

## Stack

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

```bash
curl http://127.0.0.1:8000/products
```

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

This is a prototype, not a production e-commerce backend. Catalog, stock and orders live in Python memory and are lost when the process restarts. The sample does not provide database transactions, concurrency-safe stock reservation, order persistence, customer accounts, authentication/authorization, payment integration, rate limiting or deployment configuration. Do not use it to process real orders.

Next engineering steps are PostgreSQL persistence with SQLAlchemy/Alembic, transactional inventory reservation, customer/order ownership, payment-provider integration, idempotency keys and broader tests.
