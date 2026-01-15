from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List

class AddressCreate(BaseModel):
    type: str # BILLING/SHIPPING
    country: str
    city: str
    street: str
    zip: str
    is_default: bool = False

class AddressResponse(AddressCreate):
    id: UUID
    customer_id: UUID
    
    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    external_ref: Optional[str] = None

class CustomerResponse(CustomerCreate):
    id: UUID
    addresses: List[AddressResponse] = []

    class Config:
        from_attributes = True
