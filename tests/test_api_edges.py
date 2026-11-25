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



@pytest.mark.parametrize("product_ids", [[True], [1.0]])
def test_order_rejects_non_integer_json_ids(client, product_ids):
    response = client.post("/orders", json={"product_ids": product_ids})
    assert response.status_code == 422
    assert client.get("/products").json()[0]["stock"] == 10


def test_separate_app_instances_do_not_share_catalog_or_orders():
    from fastapi.testclient import TestClient

    from main import create_app

    with TestClient(create_app()) as first_client, TestClient(create_app()) as second_client:
        first_order = first_client.post("/orders", json={"product_ids": [1]})

        assert first_order.status_code == 201
        assert first_order.json()["order_id"] == 1
        assert first_client.get("/products").json()[0]["stock"] == 9

        assert second_client.get("/products").json()[0]["stock"] == 10
        second_order = second_client.post("/orders", json={"product_ids": [1]})
        assert second_order.status_code == 201
        assert second_order.json()["order_id"] == 1
