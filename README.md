# E-commerce API Prototype

A small Python/FastAPI learning project that models a minimal product catalog and order-submission endpoint. The current implementation is intentionally simple and uses in-memory Python lists.

## Current implementation

- `GET /products`: returns the sample product list.
- `POST /orders`: accepts an order payload and appends it to an in-memory list.
- Pydantic models validate the product and order request structures.

## Stack

- Python
- FastAPI
- Pydantic

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
```

OpenAPI documentation is available at http://127.0.0.1:8000/docs.

## Example requests

```bash
curl http://127.0.0.1:8000/products
```

```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"order_id": 101, "product_ids": [1], "total": 999.99}'
```

## Important limitations

This repository is currently a prototype, not a production e-commerce backend. Data is lost when the process restarts. There is no database, inventory reservation, transactional order processing, authentication, authorization, automated test suite, CI pipeline or deployment configuration in the current implementation.

## Suggested next steps

1. Move persistence to PostgreSQL with SQLAlchemy.
2. Add product, order and order-item entities with database constraints.
3. Implement transactional stock validation and order creation.
4. Add authentication/authorization, request validation and error handling.
5. Add automated tests, migrations, Docker Compose and CI.

