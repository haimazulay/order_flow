import pytest
from fastapi.testclient import TestClient
import respx
from httpx import Response
import sys
import os

# Add parent directory to sys.path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


@pytest.fixture
def mock_services(respx_mock):
    """Mock downstream services"""
    # Customer Service Mocks
    respx_mock.get("http://localhost:8001/customers").mock(
        return_value=Response(200, json=[{"id": "1", "name": "Mock Cust", "email": "mock@test.com"}])
    )
    respx_mock.post("http://localhost:8001/customers").mock(
        return_value=Response(201, json={"id": "new-1", "name": "New Cust", "email": "new@test.com"})
    )
    
    # Order Service Mocks
    respx_mock.get("http://localhost:8002/orders").mock(
        return_value=Response(200, json=[{"id": "o1", "title": "Mock Order", "status": "PENDING"}])
    )
    return respx_mock

@respx.mock
def test_gateway_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200

@respx.mock
def test_list_customers_proxy():
    # Mock specific for this test if needed, or rely on fixture
    respx.get("http://localhost:8001/customers").mock(
        return_value=Response(200, json=[{"id": "1", "name": "M", "email": "e"}])
    )
    
    response = client.get("/api/customers")
    assert response.status_code == 200
    assert response.json() == [{"id": "1", "name": "M", "email": "e"}]

@respx.mock
def test_create_customer_proxy():
    respx.post("http://localhost:8001/customers").mock(
        return_value=Response(201, json={"id": "2", "name": "Alice"})
    )
    
    response = client.post("/api/customers", json={"name": "Alice", "email": "alice@ex.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

@respx.mock
def test_list_orders_proxy():
    respx.get("http://localhost:8002/orders").mock(
        return_value=Response(200, json=[])
    )
    resp = client.get("/api/orders")
    assert resp.status_code == 200
    assert resp.json() == []

@respx.mock
def test_create_order_proxy():
    respx.post("http://localhost:8002/orders").mock(
        return_value=Response(201, json={"id": "o2", "title": "O2"})
    )
    
    resp = client.post("/api/orders", json={"customer_id": "c1", "title": "O2"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "O2"

@respx.mock
def test_downstream_failure():
    # Simulate downtime
    respx.get("http://localhost:8001/customers").mock(side_effect=Exception("Connection Error"))
    
    # Note: main.py catches request errors and returns 503
    # except httpx.RequestError: raise HTTPException(status_code=503)
    # We need to make sure our mock triggers httpx.RequestError
    
    # Actually, respx side_effect=Exception might not be strictly a RequestError depending on type.
    # Let's import httpx
    import httpx
    respx.get("http://localhost:8001/customers").mock(side_effect=httpx.ConnectError("Fail"))

    resp = client.get("/api/customers")
    assert resp.status_code == 503
