import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
