import pytest
from fastapi.testclient import TestClient

from main import create_app


def test_list_products_returns_catalog(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["stock"] == 10


def test_create_order_calculates_total_and_reserves_stock(client):
    response = client.post("/orders", json={"product_ids": [1]})

    assert response.status_code == 201
    assert response.json() == {
        "order_id": 1,
        "product_ids": [1],
        "total": "999.99",
        "status": "accepted",
    }
    assert client.get("/products").json()[0]["stock"] == 9


def test_create_order_rejects_unknown_product(client):
    response = client.post("/orders", json={"product_ids": [999]})

    assert response.status_code == 404
    assert client.get("/products").json()[0]["stock"] == 10


def test_create_order_rejects_out_of_stock_product(client):
    client.app.state.products[0].stock = 0

    response = client.post("/orders", json={"product_ids": [1]})

    assert response.status_code == 409
    assert client.get("/products").json()[0]["stock"] == 0


def test_create_order_rejects_empty_or_duplicate_product_ids(client):
    assert client.post("/orders", json={"product_ids": []}).status_code == 422
    assert client.post("/orders", json={"product_ids": [1, 1]}).status_code == 422


@pytest.mark.parametrize("product_ids", [[0], [-1], [True], [1.0]])
def test_create_order_rejects_non_positive_or_non_integer_ids(client, product_ids):
    response = client.post("/orders", json={"product_ids": product_ids})

    assert response.status_code == 422


def test_create_order_rejects_unexpected_fields(client):
    response = client.post(
        "/orders",
        json={"product_ids": [1], "total": "0.01"},
    )

    assert response.status_code == 422


def test_each_app_instance_has_independent_catalog_and_orders(client):
    client.post("/orders", json={"product_ids": [1]})

    other_client = TestClient(create_app())
    try:
        assert other_client.get("/products").json()[0]["stock"] == 10
        second_order = other_client.post("/orders", json={"product_ids": [1]})
        assert second_order.json()["order_id"] == 1
    finally:
        other_client.close()
