import os
import sys
import pytest
import httpx
from fastapi.testclient import TestClient
from httpx import Response

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["CUSTOMER_SERVICE_URL"] = "http://customer:8001"
os.environ["ORDER_SERVICE_URL"] = "http://order:8002"

from main import app  # noqa: E402

client = TestClient(app)

@pytest.fixture
def mock_services(respx_mock):
    respx_mock.get("http://customer:8001/customers").mock(
        return_value=Response(200, json=[{"id": "1", "name": "Mock Cust", "email": "mock@test.com"}])
    )
    respx_mock.post("http://customer:8001/customers").mock(
        return_value=Response(201, json={"id": "new-1", "name": "New Cust", "email": "new@test.com"})
    )
    respx_mock.get("http://order:8002/orders").mock(
        return_value=Response(200, json=[{"id": "o1", "title": "Mock Order", "status": "PENDING"}])
    )
    respx_mock.post("http://order:8002/orders").mock(
        return_value=Response(201, json={"id": "o2", "title": "O2"})
    )
    return respx_mock

def test_gateway_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200

def test_list_customers_proxy(mock_services):
    resp = client.get("/api/customers")
    assert resp.status_code == 200
    assert resp.json()[0]["id"] == "1"

def test_create_customer_proxy(mock_services):
    resp = client.post("/api/customers", json={"name": "Alice", "email": "alice@ex.com"})
    assert resp.status_code == 200
    assert resp.json()["id"] == "new-1"

def test_list_orders_proxy(mock_services):
    resp = client.get("/api/orders")
    assert resp.status_code == 200
    assert resp.json()[0]["id"] == "o1"

def test_create_order_proxy(mock_services):
    resp = client.post("/api/orders", json={"customer_id": "c1", "title": "O2"})
    assert resp.status_code == 200
    assert resp.json()["id"] == "o2"

def test_downstream_failure(respx_mock):
    respx_mock.get("http://customer:8001/customers").mock(
        side_effect=httpx.ConnectError("Fail")
    )
    resp = client.get("/api/customers")
    assert resp.status_code == 503
