import pytest


@pytest.mark.parametrize("product_ids", [[0], [-1], [1] * 51])
def test_order_rejects_out_of_range_product_ids(client, product_ids):
    response = client.post("/orders", json={"product_ids": product_ids})
    assert response.status_code == 422


def test_order_rejects_client_supplied_total(client):
    response = client.post("/orders", json={"product_ids": [1], "total": "0.01"})

    assert response.status_code == 422
    assert client.get("/products").json()[0]["stock"] == 10


def test_order_ids_increase_after_successful_orders(client):
    first = client.post("/orders", json={"product_ids": [1]})
    second = client.post("/orders", json={"product_ids": [1]})

    assert first.status_code == second.status_code == 201
    assert first.json()["order_id"] == 1
    assert second.json()["order_id"] == 2


def test_failed_order_does_not_create_order_or_decrement_stock(client):
    client.app.state.products[0].stock = 0

    response = client.post("/orders", json={"product_ids": [1]})

    assert response.status_code == 409
    assert client.app.state.orders == []
    assert client.app.state.products[0].stock == 0
