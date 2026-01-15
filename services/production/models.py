from sqlalchemy import Column, String, Boolean, DateTime, func, Numeric, Text, ForeignKey, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship
import uuid
import enum

class Base(DeclarativeBase):
    pass

class StationType(str, enum.Enum):
    PRODUCTION = "PRODUCTION"
    PACKING = "PACKING"
    SHIPPING = "SHIPPING"

class WorkOrderState(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    REJECTED = "REJECTED"

class TaskState(str, enum.Enum):
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"
    FAILED = "FAILED"

class TaskType(str, enum.Enum):
    BUILD = "BUILD"
    PACK = "PACK"
    DISPATCH = "DISPATCH"
    QC = "QC"

class Station(Base):
    __tablename__ = "stations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    type = Column(Enum(StationType), nullable=False)
    active = Column(Boolean, default=True)

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False) # Ref to Order Service
    current_stage = Column(Enum(StationType), default=StationType.PRODUCTION)
    state = Column(Enum(WorkOrderState), default=WorkOrderState.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tasks = relationship("WorkTask", back_populates="work_order", cascade="all, delete-orphan")
    rejections = relationship("Rejection", back_populates="work_order")

class WorkTask(Base):
    __tablename__ = "work_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), nullable=False)
    station_id = Column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=True) # Assigned station
    task_type = Column(Enum(TaskType), nullable=False)
    state = Column(Enum(TaskState), default=TaskState.TODO)
    assigned_to = Column(String, nullable=True) # User/Worker ID
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    failure_reason = Column(Text, nullable=True)

    work_order = relationship("WorkOrder", back_populates="tasks")

class Rejection(Base):
    __tablename__ = "rejections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), nullable=False)
    category = Column(String, nullable=False) # Enum in simplified form here
    details = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    work_order = relationship("WorkOrder", back_populates="rejections")
