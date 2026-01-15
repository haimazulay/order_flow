from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db, engine

# Create tables if not using Alembic (for quick verify), but we use Alembic.
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service", version="1.0.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    # In real world: check db
    return {"status": "ok"}

@app.post("/customers", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers", response_model=List[schemas.CustomerResponse])
def list_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Customer).offset(skip).limit(limit).all()
