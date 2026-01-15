from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db, engine
import uuid

app = FastAPI(title="Production Service", version="1.0.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"status": "ok"}

@app.post("/work-orders", response_model=schemas.WorkOrderResponse, status_code=status.HTTP_201_CREATED)
def create_work_order(work_order: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
    db_work_order = models.WorkOrder(order_id=work_order.order_id)
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order

@app.get("/work-orders/{id}", response_model=schemas.WorkOrderResponse)
def get_work_order(id: str, db: Session = Depends(get_db)):
    db_wo = db.query(models.WorkOrder).filter(models.WorkOrder.id == id).first()
    if db_wo is None:
        raise HTTPException(status_code=404, detail="Work Order not found")
    return db_wo

@app.post("/work-orders/{id}/tasks", response_model=schemas.WorkTaskResponse)
def create_task(id: str, task: schemas.WorkTaskCreate, db: Session = Depends(get_db)):
    db_wo = db.query(models.WorkOrder).filter(models.WorkOrder.id == id).first()
    if db_wo is None:
        raise HTTPException(status_code=404, detail="Work Order not found")
    
    db_task = models.WorkTask(**task.model_dump(), work_order_id=db_wo.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.post("/tasks/{id}/complete", response_model=schemas.WorkTaskResponse)
def complete_task(id: str, db: Session = Depends(get_db)):
    db_task = db.query(models.WorkTask).filter(models.WorkTask.id == id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.state = models.TaskState.DONE
    # Logic to move WorkOrder state could be here
    db.commit()
    db.refresh(db_task)
    return db_task
