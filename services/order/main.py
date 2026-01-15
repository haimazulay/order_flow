from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db, engine
import uuid
import random

app = FastAPI(title="Order Service", version="1.0.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"status": "ok"}

@app.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Generate Order Number
    order_number = f"OF-2026-{random.randint(1000, 9999)}"
    
    db_order = models.Order(
        order_number=order_number,
        customer_id=order.customer_id,
        priority=order.priority,
        notes=order.notes
    )
    db.add(db_order)
    db.flush() # get id

    for item in order.items:
        line_total = item.unit_price * item.quantity
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            product_sku=item.product_sku,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            line_total=line_total
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
