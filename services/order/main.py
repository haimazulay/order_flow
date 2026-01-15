import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service")

# In-memory database
orders = []

class OrderCreate(BaseModel):
    customer_id: str
    title: str

class OrderResponse(BaseModel):
    id: str
    customer_id: str
    title: str
    status: str

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/orders", response_model=list[OrderResponse])
def get_orders():
    return orders

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate):
    new_order = {
        "id": str(uuid.uuid4()),
        "customer_id": order.customer_id,
        "title": order.title,
        "status": "PENDING"
    }
    orders.append(new_order)
    return new_order

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    for o in orders:
        if o["id"] == order_id:
            return o
    raise HTTPException(status_code=404, detail="Order not found")
