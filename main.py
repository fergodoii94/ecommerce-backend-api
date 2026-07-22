from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class Order(BaseModel):
    order_id: int
    product_ids: List[int]
    total: float

products = [{ "id": 1, "name": "Laptop", "price": 999.99, "stock": 10 }]
orders = []

@app.get("/products")
def list_products(): return products

@app.post("/orders")
def create_order(order: Order):
    orders.append(order)
    return {"status": "Order placed successfully", "order_id": order.order_id}
