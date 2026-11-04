import pytest

from main import orders, products


@pytest.fixture(autouse=True)
def reset_in_memory_state():
    products[0].stock = 10
    orders.clear()
