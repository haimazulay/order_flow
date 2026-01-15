from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from enum import Enum
from decimal import Decimal

class OrderStatus(str, Enum):
    NEW = "NEW"
    CONFIRMED = "CONFIRMED"
    IN_PRODUCTION = "IN_PRODUCTION"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class OrderPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

class OrderItemCreate(BaseModel):
    product_id: UUID
    product_sku: str
    product_name: str
    unit_price: Decimal
    quantity: int

class OrderItemResponse(OrderItemCreate):
    id: UUID
    line_total: Decimal

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_id: UUID
    items: List[OrderItemCreate]
    priority: OrderPriority = OrderPriority.NORMAL
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: UUID
    order_number: str
    customer_id: UUID
    status: OrderStatus
    priority: OrderPriority
    items: List[OrderItemResponse]
    created_at: object # datetime

    class Config:
        from_attributes = True
