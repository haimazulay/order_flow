import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to sys.path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, orders, create_order, OrderCreate

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_data():
    """Clear the in-memory database before each test."""
    orders.clear()
    yield
    orders.clear()

# --- Unit Tests ---
def test_create_order_logic():
    """Test the internal logic of creating an order."""
    payload = OrderCreate(customer_id="cust-123", title="My Order")
    result = create_order(payload)
    
    assert result["title"] == "My Order"
    assert result["status"] == "PENDING"
    assert "id" in result
    
    # Data consistency
    assert len(orders) == 1
    assert orders[0]["customer_id"] == "cust-123"

# --- API Tests ---
def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_api_create_order():
    response = client.post("/orders", json={"customer_id": "cust-999", "title": "API Order"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "API Order"
    assert data["status"] == "PENDING"

    # Verify persist
    get_resp = client.get("/orders")
    assert len(get_resp.json()) == 1

def test_get_order_by_id():
    # Create
    create_resp = client.post("/orders", json={"customer_id": "c1", "title": "T1"})
    order_id = create_resp.json()["id"]
    
    # Get
    resp = client.get(f"/orders/{order_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "T1"

def test_get_non_existent_order():
    resp = client.get("/orders/bad-id")
    assert resp.status_code == 404
