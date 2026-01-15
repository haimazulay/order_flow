from fastapi import FastAPI, Request, HTTPException, status
import httpx
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str = "http://auth-service:8000"
    CUSTOMER_SERVICE_URL: str = "http://customer-service:8000"
    CATALOG_SERVICE_URL: str = "http://catalog-service:8000"
    ORDER_SERVICE_URL: str = "http://order-service:8000"
    PRODUCTION_SERVICE_URL: str = "http://production-service:8000"

settings = Settings()
app = FastAPI(title="API Gateway", version="1.0.0")
client = httpx.AsyncClient()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
async def readyz():
    # Check dependencies?
    return {"status": "ok"}

async def proxy_request(url: str, method: str, body=None, headers=None):
    try:
        resp = await client.request(method, url, json=body, headers=headers)
        return resp.json(), resp.status_code
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(exc)}")

@app.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    resp, code = await proxy_request(f"{settings.AUTH_SERVICE_URL}/auth/login", "POST", body)
    if code != 200:
        raise HTTPException(status_code=code, detail=resp)
    return resp

# Example generic proxy for customers
@app.get("/api/v1/customers")
async def list_customers(request: Request):
    resp, code = await proxy_request(f"{settings.CUSTOMER_SERVICE_URL}/customers", "GET")
    if code != 200:
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.post("/api/v1/customers")
async def create_customer(request: Request):
    body = await request.json()
    resp, code = await proxy_request(f"{settings.CUSTOMER_SERVICE_URL}/customers", "POST", body)
    if code != 201:
        raise HTTPException(status_code=code, detail=resp)
    return resp

@app.get("/dashboard/overview")
async def dashboard():
    # Aggregate data
    return {
        "orders_count": 12, # Mock
        "urgent_orders": 2,
        "late_shipments": 0,
        "revenue": 15000.00
    }
