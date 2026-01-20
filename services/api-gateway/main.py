import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import json
import logging
import time

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)

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

async def proxy(request: Request, url: str, method: str, body=None):
    try:
        async with httpx.AsyncClient() as client:
            headers = {"x-request-id": getattr(request.state, "request_id", "")}
            resp = await client.request(method, url, json=body, headers=headers)
        return resp.json(), resp.status_code
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)

    logger.info(json.dumps({
        "service": "api-gateway",
        "method": request.method,
        "path": str(request.url.path),
        "status": response.status_code,
        "duration_ms": duration_ms,
        "request_id": request.headers.get("x-request-id", "")
    }))
    return response

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response

@app.get("/metrics")
def metrics():
    return "metrics_ready 1\n"

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
# Proxy to Customer Service
@app.get("/api/customers")
async def list_customers(request: Request):
    data, code = await proxy(request, f"{CUSTOMER_SERVICE_URL}/customers", "GET")
    return data

@app.post("/api/customers")
async def create_customer(request: Request):
    body = await request.json()
    data, code = await proxy(request, f"{CUSTOMER_SERVICE_URL}/customers", "POST", body)
    return data

# Proxy to Order Service
@app.get("/api/orders")
async def list_orders(request: Request):
    data, code = await proxy(request, f"{ORDER_SERVICE_URL}/orders", "GET")
    return data

@app.post("/api/orders")
async def create_order(request: Request):
    body = await request.json()
    data, code = await proxy(request, f"{ORDER_SERVICE_URL}/orders", "POST", body)
    return data
