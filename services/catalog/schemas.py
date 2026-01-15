from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from decimal import Decimal

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    unit_price: Decimal
    active: bool = True

class ProductResponse(ProductCreate):
    id: UUID
    
    class Config:
        from_attributes = True
