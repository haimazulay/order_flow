import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import logging
import time

logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Customer Service")

# In-memory database
customers = []

class CustomerCreate(BaseModel):
    name: str
    email: str

class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str

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

@app.get("/metrics")
def metrics():
    return "metrics_ready 1\n"

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/customers", response_model=list[CustomerResponse])
def get_customers():
    return customers

@app.post("/customers", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate):
    new_customer = {
        "id": str(uuid.uuid4()),
        "name": customer.name,
        "email": customer.email
    }
    customers.append(new_customer)
    return new_customer

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str):
    for c in customers:
        if c["id"] == customer_id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found")
