from decimal import Decimal
from typing import Literal

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator


class Product(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=120)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(ge=0)


class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_ids: list[StrictInt] = Field(min_length=1, max_length=50)

    @field_validator("product_ids")
    @classmethod
    def product_ids_must_be_positive(cls, value: list[int]) -> list[int]:
        if any(product_id <= 0 for product_id in value):
            raise ValueError("Product IDs must be positive integers")
        return value

    @field_validator("product_ids")
    @classmethod
    def product_ids_must_be_unique(cls, value: list[int]) -> list[int]:
        if len(value) != len(set(value)):
            raise ValueError("Duplicate product IDs are not supported")
        return value


class OrderRead(BaseModel):
    order_id: int
    product_ids: list[int]
    total: Decimal
    status: Literal["accepted"] = "accepted"


def create_app() -> FastAPI:
    app = FastAPI(title="E-commerce API Prototype", version="0.3.0")
    app.state.products = [
        Product(
            id=1,
            name="Laptop",
            price=Decimal("999.99"),
            stock=10,
        )
    ]
    app.state.orders: list[OrderRead] = []

    @app.get("/products", response_model=list[Product])
    def list_products(request: Request) -> list[Product]:
        return request.app.state.products

    @app.post(
        "/orders",
        response_model=OrderRead,
        status_code=status.HTTP_201_CREATED,
    )
    def create_order(order: OrderCreate, request: Request) -> OrderRead:
        products: list[Product] = request.app.state.products
        orders: list[OrderRead] = request.app.state.orders
        catalog = {product.id: product for product in products}
        missing_ids = [
            product_id
            for product_id in order.product_ids
            if product_id not in catalog
        ]
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "Product not found", "product_ids": missing_ids},
            )

        unavailable_ids = [
            product_id
            for product_id in order.product_ids
            if catalog[product_id].stock < 1
        ]
        if unavailable_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "Product out of stock",
                    "product_ids": unavailable_ids,
                },
            )

        total = sum(
            (catalog[product_id].price for product_id in order.product_ids),
            start=Decimal("0.00"),
        )
        for product_id in order.product_ids:
            catalog[product_id].stock -= 1

        created_order = OrderRead(
            order_id=len(orders) + 1,
            product_ids=order.product_ids,
            total=total,
        )
        orders.append(created_order)
        return created_order

    return app


app = create_app()
