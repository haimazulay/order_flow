from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from enum import Enum
from datetime import datetime

class StationType(str, Enum):
    PRODUCTION = "PRODUCTION"
    PACKING = "PACKING"
    SHIPPING = "SHIPPING"

class WorkOrderState(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    REJECTED = "REJECTED"

class TaskState(str, Enum):
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"
    FAILED = "FAILED"

class TaskType(str, Enum):
    BUILD = "BUILD"
    PACK = "PACK"
    DISPATCH = "DISPATCH"
    QC = "QC"

class WorkOrderCreate(BaseModel):
    order_id: UUID

class WorkTaskCreate(BaseModel):
    task_type: TaskType
    station_id: Optional[UUID] = None

class WorkTaskResponse(WorkTaskCreate):
    id: UUID
    work_order_id: UUID
    state: TaskState
    
    class Config:
        from_attributes = True

class WorkOrderResponse(WorkOrderCreate):
    id: UUID
    state: WorkOrderState
    tasks: List[WorkTaskResponse] = []

    class Config:
        from_attributes = True
