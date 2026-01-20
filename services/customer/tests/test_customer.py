import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to sys.path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, customers, create_customer, CustomerCreate

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_data():
    """Clear the in-memory database before each test."""
    customers.clear()
    yield
    customers.clear()

# --- Unit Tests ---
def test_create_customer_logic():
    """Test the internal logic of creating a customer (data-level)."""
    payload = CustomerCreate(name="Unit Test User", email="unit@test.com")
    result = create_customer(payload)
    
    # Verify return object
    assert result["name"] == "Unit Test User"
    assert "id" in result
    
    # Verify in-memory state (Data-level test)
    assert len(customers) == 1
    assert customers[0]["email"] == "unit@test.com"

# --- API Tests ---
def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_api_create_customer():
    response = client.post("/customers", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data
    
    # Verify it persists via API
    get_resp = client.get("/customers")
    assert len(get_resp.json()) == 1

def test_get_customer_by_id():
    # Create first
    create_resp = client.post("/customers", json={"name": "Bob", "email": "bob@example.com"})
    customer_id = create_resp.json()["id"]
    
    # Get by ID
    resp = client.get(f"/customers/{customer_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Bob"

def test_get_non_existent_customer():
    resp = client.get("/customers/non-existent-id")
    assert resp.status_code == 404
