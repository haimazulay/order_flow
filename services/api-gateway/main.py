import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="API Gateway")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://customer:8001")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order:8002")

async def proxy(url: str, method: str, body=None):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.request(method, url, json=body)
        return resp.json(), resp.status_code
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
# Proxy to Customer Service
@app.get("/api/customers")
async def list_customers():
    data, code = await proxy(f"{CUSTOMER_SERVICE_URL}/customers", "GET")
    return data

@app.post("/api/customers")
async def create_customer(request: Request):
    body = await request.json()
    data, code = await proxy(f"{CUSTOMER_SERVICE_URL}/customers", "POST", body)
    return data

# Proxy to Order Service
@app.get("/api/orders")
async def list_orders():
    data, code = await proxy(f"{ORDER_SERVICE_URL}/orders", "GET")
    return data

@app.post("/api/orders")
async def create_order(request: Request):
    body = await request.json()
    data, code = await proxy(f"{ORDER_SERVICE_URL}/orders", "POST", body)
    return data
