from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_products_returns_catalog():
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["stock"] == 10


def test_create_order_calculates_total_and_reserves_stock():
    response = client.post("/orders", json={"product_ids": [1]})

    assert response.status_code == 201
    assert response.json() == {
        "order_id": 1,
        "product_ids": [1],
        "total": "999.99",
        "status": "accepted",
    }
    assert client.get("/products").json()[0]["stock"] == 9


def test_create_order_rejects_unknown_product():
    response = client.post("/orders", json={"product_ids": [999]})

    assert response.status_code == 404
    assert client.get("/products").json()[0]["stock"] == 10


def test_create_order_rejects_out_of_stock_product():
    from main import products

    products[0].stock = 0
    response = client.post("/orders", json={"product_ids": [1]})

    assert response.status_code == 409
    assert client.get("/products").json()[0]["stock"] == 0


def test_create_order_rejects_empty_or_duplicate_product_ids():
    assert client.post("/orders", json={"product_ids": []}).status_code == 422
    assert client.post("/orders", json={"product_ids": [1, 1]}).status_code == 422
